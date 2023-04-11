import universal_functions as uf
import torch
import re

# global
cos = torch.nn.CosineSimilarity(dim=0)
# kmeans_folder = uf.get_files_from_folder(f"{uf.nep_location}BertClusteringClassification\\KmeansOutput\\Diff_percent", 'pkl')
# kmeans_file = [f"{uf.nep_location}BertClusteringClassification\\KmeansOutput\\Diff_percent\\",f"_EmbCOMPLETE_Kmeans_0.3.pkl"]

# Helper function
def get_dataset_year(ds_name):
    try:
        regex = r"(?<=\-)(.*?)(?=\_)"
        year = re.findall(regex, ds_name)[0]
    except IndexError:
        year = ds_name.split('-')[-1]
    return int(year)

def find_represented_datasets(data:dict)->dict:
    datasets = {} # Take dict of cluster_id: dataset names and turn it into a dict with dataset_name: cluster_id
    for k in data.keys():
        for elt in data[k]:
            if elt[0] not in datasets.keys():
                datasets[elt[0]] =[]
            if elt[1] not in datasets[elt[0]]:
                datasets[elt[0]].append(elt[1])
    return datasets


def get_kmeans_data(dataset_name:str, topic:str, kmeans_folder:list)->list:
    # filename = f"{uf.nep_location}\\BertClusteringClassification\\KmeansOutput\\{dataset_name}_EmbCOMPLETE_Kmeans.pkl"
    # filename = kmeans_file[0]+dataset_name+kmeans_file[1]
    kmeans_loc = [x for x in kmeans_folder if f"\\{dataset_name}" in x]
    kmeans_data = uf.import_pkl_file(kmeans_loc[-1])[topic] # 11111
    return kmeans_data['cluster_centers'] # get list of cluster center embeddings given dataset name & topic

def find_matching_narratives(cluster_center, query_dataset:str, topic:str, kmeans_folder)->list:
    results = []

    query_year =get_dataset_year(query_dataset)

    for file in kmeans_folder: # Iterate through the kmeans file names
        cand_dataset_name = uf.get_dataset_id(file)
        year = get_dataset_year(cand_dataset_name)
        if query_dataset not in file and query_year < year: # If the kmeans file is not the same as the query & is from a later year...
            try:
                cand_data = uf.import_pkl_file(file)[topic]['cluster_centers'] # load cluster center data
            except KeyError:
                continue # Happens when a topic (like Transphobia) does not appear in the dataset
            for i in range(len(cand_data)): # Iterate through the cluster centers of the later file
                sim = cos(torch.from_numpy(cand_data[i]), torch.from_numpy(cluster_center))
                if sim > 0.97:
                    results.append([cand_dataset_name, i]) # Add a match if the cluster centers are very similar
    return results

# Secondary function
def get_second_steps(first_step_data:dict, topic:str, kmeans_folder):
    results = {} # Initialize results variables

    datasets = find_represented_datasets(first_step_data)

    for k in datasets.keys(): # Iterate through the datasteps found in first step tracking
        results[k] = {}
        try:
            cluster_centers = get_kmeans_data(k, topic, kmeans_folder)  # Get kmeans file
        except FileNotFoundError:
            continue

        for cl in datasets[k]: # Iterate through the cluster ids for the found datsets
            try:
                query_narrative = cluster_centers[cl] # load the embedding representation for the cluster id
                results[k][cl] = find_matching_narratives(query_narrative, k, topic, kmeans_folder)
            except IndexError:
                continue
    # Clean up final results by eliminating empty lists
    final = {}
    for key in results.keys():
        counts = False
        for cluster in results[key].keys():
            if results[key][cluster] != []: # If the cluster is not empty
                counts = True # indicate that it should be included in the final dict
        if counts == True:
            final[key] = results[key]
    return final

# Main function
def run_second_step_tracking(first_step, kmeans_folder,clustering_type,embedding_type):
    if embedding_type:
        kmeans_cleaned = [x for x in kmeans_folder if embedding_type in x]
        if "BertClusteringClassification" in kmeans_folder[0]:
            if clustering_type =="0.2":
                kmeans_cleaned = [x for x in kmeans_cleaned if  "0.3" not in x]
            elif clustering_type=="0.3":
                kmeans_cleaned = [x for x in kmeans_cleaned if "0.2" not in x]
        else:
            kmeans_cleaned = [x for x in kmeans_cleaned if clustering_type in x]
    else:
        kmeans_cleaned = [x for x in kmeans_folder if 'emoji' not in x and
                          'parentheses' not in x and 'separated' not in x]
        if "BertClusteringClassification" in kmeans_folder[0]:
            if clustering_type =="0.2":
                kmeans_cleaned = [x for x in kmeans_cleaned if  "0.3" not in x]
            elif clustering_type=="0.3":
                kmeans_cleaned = [x for x in kmeans_cleaned if "0.3" in x]
        else:
            kmeans_cleaned = [x for x in kmeans_cleaned if clustering_type in x]
    second_steps = {} #11111
    for key in first_step.keys():
        second_steps[key] = get_second_steps(first_step_data=first_step[key], topic=key, kmeans_folder=kmeans_cleaned)

    return second_steps