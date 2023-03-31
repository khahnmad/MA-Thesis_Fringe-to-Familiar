import json
import re

from Reconstruction_Phase.Vectorization import BERT_model as b
import universal_functions as uf
from config import import_functions as imp

# Global variables
sro_dir = uf.repo_loc / 'Deconstruction_Phase/SRO_Instances'

reconstruction_dir = uf.repo_loc / 'Reconstruction_Phase'

reduced_sro_dir = reconstruction_dir / 'Vectorization/Reduced_SRO'
embeddings_dir = reconstruction_dir / 'Vectorization/Embeddings'


def fetch_similar_triplets(data, article_id, sentence_id):
    same_sent = [x for x in data if x['article_id'] == article_id and x['sentence_id'] == sentence_id]

    removable, to_save = [],[]
    for i in range(len(same_sent)):
        if i not in removable:
            to_save.append(same_sent[i])
            i_recreation = f"{same_sent[i]['subject']} {same_sent[i]['relation']} {same_sent[i]['object']}".lower().split(' ')
            for j in range(len(same_sent)):
                if i != j:
                    j_recreation = f"{same_sent[j]['subject']} {same_sent[j]['relation']} {same_sent[j]['object']}".lower().split(' ')
                    i_intersection = set(i_recreation).intersection(j_recreation)
                    j_intersection = set(j_recreation).intersection(i_intersection)
                    j_percent = len(i_intersection)/len(j_recreation)
                    oppostite_interse =  len(j_intersection)/len(i_recreation)
                    if j_percent > 0.6 and oppostite_interse > 0.6:
                        removable.append(j)

    return to_save


def remove_extra_sentences(topic, dataset_name, clean_data, starting_point, id_record):
    # just getting the first one - maybe there's a better way
    # Get highest checkpoint

    # id_record = []
    # clean_data = []
    for i in range(starting_point, len(topic)):
        elt = topic[i]
        index = f"{elt['article_id']}.{elt['sentence_id']}"

        if index not in id_record:
            # fetch toher triplets from that sentence
            similar_triplets = fetch_similar_triplets(topic, elt['article_id'],elt['sentence_id'])
            clean_data+=similar_triplets
            id_record.append(index)
        if str(i).endswith('0000'): # TODO is that a good number?
            print(f"    Dumping checkpoint at {i}.... {(i/len(topic))*100}% complete")
            export_name = str(reduced_sro_dir / f"{dataset_name}_Reduced_SROs_checkpoint_{i}.json")
            a_content = json.dumps({'content': {"clean_data":clean_data, "id_record":id_record}})
            uf.export_as_json(export_name, a_content)
    return clean_data


def reduce_data(dataset_name, loc):
    export_name = reduced_sro_dir / f"{dataset_name}_Reduced_SROs.json"
    prev_files = [str(x) for x in list(reduced_sro_dir.iterdir())]

    if export_name in prev_files:
        print(f'    Importing reduced data for {dataset_name}...')
        sro_data = uf.import_json_content(export_name)
    else:

        print(f'    Reducing data from {dataset_name}...')

        sro_data = imp.import_SRO_data_from_file(loc, as_dict=True)
        sro_data = [x for x in uf.flatten_list(sro_data) if isinstance(x, str) == False]
        existing_data, start_point= find_highest_prevfile(loc)
        if existing_data=='complete':
            print(f'    Importing reduced data for {dataset_name}...')
            sro_data = uf.import_json_content(export_name)
            return sro_data
        sro_data = remove_extra_sentences(sro_data, dataset_name, clean_data=existing_data['clean_data'], starting_point=start_point,
                                          id_record=existing_data['id_record'])

        a_content = json.dumps({'content': sro_data})
        uf.export_as_json(str(export_name), a_content)

    return sro_data


def find_highest_checkpoint(filename):
    # NOTE: THIS IS FROM BEFORE I CHANGED TO USING THE REDUCED SYSTEM
    dataset_name = uf.get_dataset_id(filename)
    prev_files = [str(x) for x in list(embeddings_dir.iterdir())]
    # TODO: Made relative

    highest = [0, None]
    for file in prev_files:
        if f"\\{dataset_name}" in file:
            if 'checkpoint' not in file:
                return 'complete','complete'
            regex = r"(?<=embeddings\_)(.*?)(?=\_)"
            checkpoint = int(re.findall(regex, file)[0])
            if checkpoint > highest[0]:
                highest = [checkpoint+1, file]
    return highest[1], highest[0]


def find_highest_prevfile(filename):
    # NOTE: THIS IS FROM BEFORE I CHANGED TO USING THE REDUCED SYSTEM
    dataset_name = uf.get_dataset_id(filename)
    prev_files = [str(x) for x in list(reduced_sro_dir.iterdir())]


    highest = [0, {"clean_data":[],"id_record":[]}]
    for file in prev_files:
        if f"\\{dataset_name}" in file:
            if 'checkpoint' not in file:
                return 'complete','complete'
            regex = r"(?<=checkpoint\_)(.*?)(?=\.json)"
            checkpoint = int(re.findall(regex, file)[0])
            if checkpoint > highest[0]:
                data = uf.import_json_content(file)
                highest = [checkpoint+1, data]
    return highest[1], highest[0] # file data, starting point

def create_embeddings():
    sro_locs = list(sro_dir.iterdir())
    for loc in sro_locs[33:]:
        print(f'Running {loc}...')

        dataset_name = uf.get_dataset_id(loc)
        sro_data = reduce_data(dataset_name, loc)

        prev_file, starting_point = find_highest_checkpoint(loc)

        if prev_file != None:
            if prev_file != 'complete':
                try:
                    embeddings = uf.import_pkl_file(prev_file)
                except EOFError:
                    print(F"EOF Error: {dataset_name}")
            else:
                print(f"{dataset_name} is complete\n") # TOdo make sure that this works,also in the find highest checkpoint function
                continue
        else:
            embeddings = []
            starting_point = 0

        embeddings = b.generate_embeddings_for_dataset(sro_data=sro_data,mode='whole_triplet',dataset_name=dataset_name,
                                          starting_point=starting_point,embeddings=embeddings)
        uf.export_as_pkl(embeddings_dir / f"{dataset_name}_embeddings.pkl", embeddings)
if __name__ == '__main__':
    create_embeddings()