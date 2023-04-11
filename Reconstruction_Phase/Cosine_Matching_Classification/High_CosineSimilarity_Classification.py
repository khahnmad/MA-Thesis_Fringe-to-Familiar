"""
This file takes files that have already been run through cosine similarity, but at too low of a number, and runs them
on a higher similarity threshold
"""
import torch
import universal_functions as uf
import re

# GLOBAL
low_cos_loc = uf.repo_loc / 'Reconstruction_Phase/Cosine_Matching_Classification/output/low'
low_cos_files = uf.get_files_from_folder(low_cos_loc, "pkl")

# old_cos_loc= f"{uf.nep_location}BertClusteringClassification\\CosineClassification"
# old_cos_w_sent_loc = f"{old_cos_loc}\\Sent_Embeddings"

high_cos_matching_loc = uf.repo_loc / 'Reconstruction_Phase/Cosine_Matching_Classification/output/high'
high_cos_files = uf.get_files_from_folder(high_cos_matching_loc, 'pkl')

key_matching_loc = uf.repo_loc / 'Reconstruction_Phase/Keyword_Matching_Classification/output'
keywordmatch_locs = uf.get_files_from_folder(key_matching_loc, 'pkl')

cos = torch.nn.CosineSimilarity(dim=0)

# HELPER FUNCTIONS
def get_checkpoint(file:str, dataset_name:str)->str:
    if "CosineMatching" in file:
        regex = fr"(?<={dataset_name}\_Emb)(.*?)(?=\_Cosine)"
        checkpoint = re.findall(regex, file)[0]
    else:
        regex = r"(?<=Emb)(.*?)(?=\.)"
        checkpoint = re.findall(regex, file)[0]
    return checkpoint # Returns the number of embeddings processed, or "COMPLETE"


def get_starting_point(filename):
    if 'checkpoint' in filename:
        regex = r"(?<=checkpoint\_)(.*?)(?=\.)"
        starting_point = re.findall(regex, filename)[0]
        return starting_point
    else:
        starting_point = 'complete'
        return starting_point


def sort_into_topics(string_matching, cosine_matching):
    classified = string_matching+cosine_matching
    topic_dict = {'Immigration':[],'Transphobia':[],'Islamophobia':[],'Anti-semitism':[]}
    for elt in classified:
        for cat in elt['Category']:
            topic_dict[cat].append(elt)
    return topic_dict


def remove_duplicates(data:dict)->dict:
    cleaned_data = {k:[] for k in data.keys()}
    already_processed = []
    count = 0

    for topic in data.keys():
        for row in data[topic]:
            unique_id = f"{row['article_id']}.{row['sentence_id']}.{row['subject']}.{row['relation']}.{row['object']}"
            if unique_id not in already_processed:
                cleaned_data[topic].append(row)
                already_processed.append(unique_id)
            else:
                count += 1
    print(f"    Found {count} duplicates to remove")
    return cleaned_data


# MAIN FUNCTION
def update_cosine_matching(filename,keyword_data):
    second_layer = []
    data = uf.import_pkl_file(filename)
    for key in data.keys(): # Iterate through the topics in the dict
        topic_inner_layer = [x for x in keyword_data['inner_layer'] if key in x['Category']]
        for i in range(len(data[key])): # Iterate through the elts in the topic
            elt = data[key][i] # Save the elt
            ex_embedding = elt['embedding'] # Save the embedding
            if ex_embedding == None:
                continue

            # Check if the embedding is a match to an inner layer emb of the same topic
            for j in range(len(topic_inner_layer)):
                in_elt = keyword_data['inner_layer'][j]
                in_embedding = keyword_data['inner_layer'][j]['embedding']
                if in_embedding ==None:
                    continue
                similarity = float(cos(ex_embedding, in_embedding))
                if similarity > 0.985:
                    elt['similarity'] = [key,similarity]
                    if elt not in second_layer:
                        second_layer.append(elt)
                    # TODO: this is where dupliates are coming in - be cautious of this
            if str(i).endswith('00'):
                print(f"        {key}: {i}")

    # IF the old cosine file was incomplete, have to get the starting point & go through the remaining unclassified
    # data
    if 'checkpoint' in filename:
        start = int(get_starting_point(filename))+1
        fresh_classifications = classify_remaining_text(unclassified_data=keyword_data['unclassified'],
                                                        inner_layer_data=keyword_data['inner_layer'],
                                                        starting_point=start)
        second_layer+=fresh_classifications
    return second_layer

def classify_remaining_text(unclassified_data, inner_layer_data, starting_point):
    # Need unclassified data
    # Need inner layer data
    # dont need second layer if we're already in the saem function
    # Need starting point
    classified = []
    for i in range(starting_point, len(unclassified_data)):
        u_embedding = unclassified_data[i]['embedding']
        if u_embedding==None:
            continue
        u_category = []

        for j in range(len(inner_layer_data)):
            embedding = inner_layer_data[j]['embedding']
            if embedding == None:
                continue
            category = inner_layer_data[j]['Category']

            similarity = float(cos(embedding, u_embedding))
            if similarity > 0.985:
                for c in category:
                    if c not in u_category:
                        u_category.append(c)

                        unclassified_data[i]['similarity '] = [c,similarity]

        unclassified_data[i]['Category'] = u_category
        if u_category != []:
            classified.append(unclassified_data[i])
    return classified

def run_cosineimilarity_update():
    for file in low_cos_files[39:]:
        dataset_name = uf.get_dataset_id(file)
        checkpoint = get_checkpoint(file,dataset_name)
        print(f"Running {dataset_name}")
        # Check if the file is already updated
        export_name = f"{str(high_cos_matching_loc)}\\{dataset_name}_Emb{checkpoint}.pkl"
        if export_name in high_cos_files:
            print("-- already complete --\n")
            continue

        # Get Keyword Match file
        keyword_matches = [x for x in keywordmatch_locs if f"\\{dataset_name}_E" in x]
        if len(keyword_matches) < 1:
            print(f"-- No Keyword Match file --\n")
            continue

        keyword_match = uf.import_pkl_file(keyword_matches[-1])

        results = update_cosine_matching(filename=file, keyword_data=keyword_match)

        sorted_dict = sort_into_topics(string_matching=keyword_match['inner_layer'],cosine_matching=results)

        final_dict = remove_duplicates(sorted_dict)
        len_final_dict = sum([len(final_dict[k]) for k in final_dict.keys()])
        print(f"   Dict now has {len_final_dict} elts, compared to {len(keyword_match['inner_layer'])} before")
        uf.export_as_pkl(export_name=export_name,content=final_dict)
