# Track where the narratives go in one step away from the origin, regardless of partisanship
import universal_functions as uf
from typing import List
import torch
import re
# GLOBAL
cos = torch.nn.CosineSimilarity(dim=0)


# HELPER FUNCTIONS
def get_dataset_year(ds_name):
    try:
        regex = r"(?<=\-)(.*?)(?=\_)"
        year = re.findall(regex, ds_name)[0]
    except IndexError:
        year = ds_name.split("-")[-1]
    return int(year)


def load_topic_from_other_datasets(category:str, year:int, kmeans_folder:list, clustering_type:str, embedding_type:str)->(list,list):
    # Find datasets from the same year or before and of the same topic
    if embedding_type:
        other_file_locs = [x for x in kmeans_folder if embedding_type in x]
        if "BertClusteringClassification" in kmeans_folder[0]:
            if clustering_type =="0.2":
                other_file_locs = [x for x in other_file_locs if  "0.3" not in x]
            elif clustering_type=="0.3":
                other_file_locs = [x for x in other_file_locs if "0.2" not in x]
        else:
            other_file_locs = [x for x in other_file_locs if clustering_type in x]
    else:
        other_file_locs = [x for x in kmeans_folder  if 'emoji' not in x and
                           'parentheses' not in x and 'separated' not in x]
        if "BertClusteringClassification" in kmeans_folder[0]:
            if clustering_type =="0.2":
                other_file_locs = [x for x in other_file_locs if  "0.3" not in x]
            elif clustering_type=="0.3":
                other_file_locs = [x for x in other_file_locs if "0.2" not in x]
        else:
            other_file_locs = [x for x in other_file_locs if clustering_type in x]
    # 11111
    datasets,filenames = [],[]
    for file in other_file_locs:
        dataset_yr = get_dataset_year(uf.get_dataset_id(file))
        if dataset_yr > year: # NOTE: only getting datasets that occur AFTER the given year
            data = uf.import_pkl_file(file)
            try:
                datasets.append(data[category])
            except KeyError:
                continue
            filenames.append(file)
    return datasets, filenames # Returns other datasets, list of corresponding file names


def track_cluster_appearances(other_datasets:List[dict], datasets_names:List[str], topic:dict, unique_clusters:List[int]):
    # Find clusters that match the origin clusters in unique clusters
    cluster_centers = topic['cluster_centers']

    # dict with keys: each of the unique cluster ids, value : list
    cluster_new_fits = {k: [] for k in unique_clusters}
    for d in range(len(other_datasets)): # Iterate through the other datasets collected from years after the query dataset
        dataset = other_datasets[d] # Format: dict with keys "narratives_classified", "num_clusters", "cluster_centers"

        dataset_name = uf.get_dataset_id(datasets_names[d]) # dataset name
        d_centers = dataset['cluster_centers'] # list of numpy arrays

        for i in unique_clusters: # Iterate through the unique clusters
            f_cent = cluster_centers[i] # Get the cluster center of the identified unique cluster

            for j in range(len(d_centers)): # Iterate through the other dataset centers
                d_cent = d_centers[j]

                sim = cos(torch.from_numpy(d_cent), torch.from_numpy(f_cent))
                if float(sim) > 0.97:  # if the two cluster centers are very similar:
                    # f_text = get_text_from_cluster(fr_narratives_classified,i)
                    # d_text = get_text_from_cluster(dataset['narratives_classified'], j)
                    cluster_new_fits[i].append([dataset_name, j])  # Add it to our list of results
    return cluster_new_fits


## MAIN FUNCTION ##

def run_first_step_tracking(starter_narratives, dataset_name, dataset_year, kmeans_folder:list,clustering_type, embedding_type):
    results = {}
    if clustering_type not in dataset_name:
        if embedding_type:
            if clustering_type=="0.3":
                kmeans_output_loc = [x for x in kmeans_folder if f"\\{dataset_name}" in x and "0.3" in x]
            elif clustering_type =="0.2":
                kmeans_output_loc = [x for x in kmeans_folder if f"\\{dataset_name}" in x and "0.3" not in x]
        else:
            if clustering_type=="0.3":
                kmeans_output_loc = [x for x in kmeans_folder if f"\\{dataset_name}" in x and "0.3" in x and 'emoji' not in x and 'parentheses' not in x]
            elif clustering_type =="0.2":
                kmeans_output_loc = [x for x in kmeans_folder if f"\\{dataset_name}" in x and "0.3" not in x and 'emoji' not in x and 'parentheses' not in x]
    else:
        if embedding_type:
            kmeans_output_loc = [x for x in kmeans_folder if f"\\{dataset_name}" in x and embedding_type in x]
        else:
            kmeans_output_loc = [x for x in kmeans_folder if f"\\{dataset_name}" in x and 'emoji' not in x and 'parentheses' not in x]
    kmeans_output = uf.import_pkl_file(kmeans_output_loc[0]) # 1111
    # Data format: dict with key: topic, value: dict with three keys: "narratives_classified", "num_clusters", & "cluster_centers"

    for cat in starter_narratives.keys():
        other_datasets, datasets_names = load_topic_from_other_datasets(cat, dataset_year,kmeans_folder, clustering_type, embedding_type)
        topic_results = track_cluster_appearances(other_datasets, datasets_names,kmeans_output[cat], starter_narratives[cat])
        results[cat] = {k:topic_results[k] for k in topic_results.keys() if topic_results[k]!=[]}

    return results
