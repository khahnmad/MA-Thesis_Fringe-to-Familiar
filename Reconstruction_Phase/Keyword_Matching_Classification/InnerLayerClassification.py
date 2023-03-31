import universal_functions as uf
from config import import_functions as imp
import re
from typing import List

reconstruction_dir = uf.repo_loc / 'Reconstruction_Phase'
matching_output_dir = reconstruction_dir / 'Keyword_Matching_Classification/output'

# GLOBAL
keyword_dict = uf.import_json_content(reconstruction_dir / 'Keyword_Identification/valid_keywords.json')
# w_sent_embeddings_loc = uf.get_files_from_folder(f"{uf.thesis_location}locally_createEmbeddings\\Sent_Embeddings","pkl")
# no_sent_emb_loc = uf.get_files_from_folder(f"{uf.thesis_location}locally_createEmbeddings\\Embeddings","pkl")
# embeddings_loc = w_sent_embeddings_loc+no_sent_emb_loc
embeddings_loc= uf.get_files_from_folder(str(reconstruction_dir / 'Vectorization/Embeddings'),'pkl')

inner_locs = uf.get_files_from_folder(str(reconstruction_dir / 'Keyword_Matching_Classification/output'), "pkl")


def find_inner_layer_classifications(embeddings:List):
    inner_layer, unclassified = [],[]
    for i in range(len(embeddings)): # Iterate through embeddings
        e = embeddings[i]
        e['Category'] = []

        for cat in keyword_dict.keys(): # Iterate through the topic categories
            keywords = keyword_dict[cat]
            for k in keywords: # Iterate through the keywords
                if k in e['subject'].lower() or k in e['relation'].lower() or k in e['object'].lower():
                    if k in [x.lower() for x in e['tokenized_sentence']] or ' ' in k:
                        e['Category'].append(cat) # If the keyword appears in the sro, add it to the category

        if e['Category'] == []:
            unclassified.append(e)
        else:
            inner_layer.append(e)
    return inner_layer, unclassified


def get_checkpoint(file:str):
    if 'checkpoint' in file:
        regex = r"(?<=embeddings\_)(.*?)(?=\_checkpoint)"
        checkpoint = int(re.findall(regex, file)[0])
        return checkpoint  # returns the number of embeddings that have so far been processed
    return 'COMPLETE'  # If the embedding collection is complete, ie there is no checkpoint in the title


def find_highest_file(filename:str, folder:List[str]):
    dataset_name = uf.get_dataset_id(filename)
    highest_file = [x for x in folder if f"\\{dataset_name}" in x][-1]
    checkpoint = get_checkpoint(highest_file)
    return highest_file, checkpoint


for loc in embeddings_loc:
    print(f"Running {loc}")
    dataset_name = uf.get_dataset_id(loc)

    # Find the embedding file with the highest number of embeddings processed
    highest_file, emb_checkpoint = find_highest_file(filename=loc, folder=embeddings_loc)

    # Check if there has already been a round of classification for this file
    export_name = str(matching_output_dir) + f"{dataset_name}_Emb{emb_checkpoint}.pkl"
    if export_name in inner_locs:
        print("-- already complete --\n")
        continue # the file has already been run

    data = imp.import_embedding_triplet_from_file(loc, as_dict=True)
    if data == None:
        print(f"    Skipping...")

    inner_layer, unclassified = find_inner_layer_classifications(embeddings=data)
    print(f"    Exporting classifications...\n")
    # Export data
    exportable = {'inner_layer':inner_layer,'unclassified':unclassified}
    uf.export_as_pkl(export_name=export_name,content=exportable)
