"""
"""
import torch
import universal_functions as uf
import re

# GLOBAL
output_loc = uf.repo_loc / 'Reconstruction_Phase/Cosine_Matching_Classification/output'
old_cos_loc = output_loc / 'low'
# old_cos_w_sent_loc = f"{old_cos_loc}\\Sent_Embeddings"

cos_matching_loc = str(output_loc / 'high')
key_matching_loc = uf.repo_loc / 'Reconstruction_Phase/Keyword_Matching_Classification/output'

keywordmatch_locs = uf.get_files_from_folder(str(key_matching_loc), 'pkl')
cos_files = uf.get_files_from_folder(str(cos_matching_loc), 'pkl')

old_cos_files = uf.get_files_from_folder(str(old_cos_loc),"pkl")

cos = torch.nn.CosineSimilarity(dim=0)


def find_similar_vectors(starting_point:int,unclassified:list,inner_layer:list, second_layer:list, dataset_name:str,
                         checkpoint:str, threshold:float,cos_loc:str):
    for i in range(starting_point, len(unclassified)):
        u_embedding = unclassified[i]['embedding']
        if u_embedding==None:
            continue
        u_category = []

        for j in range(len(inner_layer)):
            embedding = inner_layer[j]['embedding']
            if embedding == None:
                continue
            category = inner_layer[j]['Category']

            similarity = float(cos(embedding, u_embedding))
            if similarity > threshold:
                for c in category:
                    if c not in u_category:
                        u_category.append(c)

        unclassified[i]['Category'] = u_category
        if u_category != []:
            second_layer.append(unclassified[i])

        if str(i).endswith("000"):
            print(f"    Dumping at checkpoint {i}")
            sorted_dict = sort_into_topics(string_matching=inner_layer, cosine_matching=second_layer)
            export_name = f"{cos_loc}\\{dataset_name}_Emb{checkpoint}_checkpoint_{i}.pkl"
            # uf.export_as_pkl(export_name, {'sorted_dict':sorted_dict, 'second_layer':second_layer})
            uf.export_as_pkl(export_name, {'sorted_dict':sorted_dict, 'second_layer':second_layer})
    return second_layer


def sort_into_topics(string_matching, cosine_matching):
    classified = string_matching+cosine_matching
    topic_dict = {'Immigration':[],'Transphobia':[],'Islamophobia':[],'Anti-semitism':[]}
    for elt in classified:
        for cat in elt['Category']:
            topic_dict[cat].append(elt)
    return topic_dict


def get_checkpoint(file:str)->str:
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


def find_incomplete_files(dataset_name, checkpoint):
    export_name = f"{cos_matching_loc}\\{dataset_name}_Emb{checkpoint}.pkl"
    if export_name in cos_files:
        return "complete"  # If the anticipated export name already exists

    prev_files = [x for x in cos_files if f"\\{dataset_name}" in x]
    if len(prev_files) > 0:
        prev_file = prev_files[-1]
        starting_point = int(get_starting_point(prev_file))+1
        return starting_point, prev_file
    else:
        return 0


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


def run_cosine_classification_low_threshold():
    for file in keywordmatch_locs:
        dataset_name = uf.get_dataset_id(file)
        checkpoint = get_checkpoint(file)
        print(f"Running {dataset_name}...")

        # Check if it is already complete
        old_file_complete = [x for x in old_cos_files if f"\\{dataset_name}_Emb{checkpoint}_Cosine" in x]
        if len(old_file_complete)>0:
            print('-- old file exists, skipping --')
            continue

        # # Check if it is already complete
        # export_name = f"{cos_matching_loc}\\{dataset_name}_Emb{checkpoint}.pkl"
        # if export_name.lower() in [x.lower() for x in cos_files]:
        #     print("-- already complete --")
        #     continue

        # Check if it partly complete
        prev_files = [x for x in old_cos_files if f"\\{dataset_name}" in x]
        if len(prev_files) > 0:
            sp = get_starting_point(prev_files[-1])
            prev_data = uf.import_pkl_file(prev_files[-1])
            if sp == 'complete':
                sec_layer = uf.flatten_list([prev_data[k] for k in prev_data.keys()])
                start = 0

            else:
                start = int(sp) + 1
                sec_layer =prev_data['second_layer']

        # Otherwise it starts from the beginning
        else:
            start = 0
            sec_layer = []

        data = uf.import_pkl_file(file)
        second_layer = find_similar_vectors(inner_layer=data['inner_layer'],unclassified=data['unclassified'],
                                            dataset_name=dataset_name,checkpoint=checkpoint,starting_point=start,
                                            second_layer=sec_layer, threshold=0.97, cos_loc=old_cos_loc)
        # Sort the matches into topics
        sorted_dict = sort_into_topics(string_matching=data['inner_layer'],cosine_matching=second_layer)

        # Remove duplicates in the dictionary
        final_dict = remove_duplicates(sorted_dict)

        # Export
        export_name = f"{old_cos_loc}\\{dataset_name}_Emb{checkpoint}.pkl"
        uf.export_as_pkl(export_name, final_dict)

def run_cosine_classification_high_threshold():
    for file in keywordmatch_locs[19:]:
        dataset_name = uf.get_dataset_id(file)
        checkpoint = get_checkpoint(file)
        print(f"Running {dataset_name}...")

        # Check if an old version has already been run, so this should be skipped & the alternate program should be run
        old_file_complete = [x for x in old_cos_files if f"\\{dataset_name}_Emb{checkpoint}" in x]
        if len(old_file_complete)>0:
            print('-- old file exists, skipping --')
            continue

        # Check if it is already complete
        export_name = f"{cos_matching_loc}\\{dataset_name}_Emb{checkpoint}.pkl"
        if export_name.lower() in [x.lower() for x in cos_files]:
            print("-- already complete --")
            continue

        # Check if it partly complete
        prev_files = [x for x in cos_files if f"\\{dataset_name}" in x]
        if len(prev_files) > 0:
            sp = get_starting_point(prev_files[-1])
            prev_data = uf.import_pkl_file(prev_files[-1])
            if sp == 'complete':
                sec_layer = uf.flatten_list([prev_data[k] for k in prev_data.keys()])
                start = 0

            else:
                start = int(sp) + 1
                sec_layer =prev_data['second_layer']

        # Otherwise it starts from the beginning
        else:
            start = 0
            sec_layer = []

        data = uf.import_pkl_file(file)
        second_layer = find_similar_vectors(inner_layer=data['inner_layer'],unclassified=data['unclassified'],
                                            dataset_name=dataset_name,checkpoint=checkpoint,starting_point=start,
                                            second_layer=sec_layer, threshold=0.985, cos_loc=cos_matching_loc)
        # Sort the matches into topics
        sorted_dict = sort_into_topics(string_matching=data['inner_layer'],cosine_matching=second_layer)

        # Remove duplicates in the dictionary
        final_dict = remove_duplicates(sorted_dict)

        # Export
        export_name = f"{cos_matching_loc}\\{dataset_name}_Emb{checkpoint}.pkl"
        uf.export_as_pkl(export_name, final_dict)

