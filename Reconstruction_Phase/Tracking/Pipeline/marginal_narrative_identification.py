# Find starter narratives, indepdent of partisanship
import universal_functions as uf
import torch
from typing import List
import json
import re

# GLOBAL
cos = torch.nn.CosineSimilarity(dim=0)
# kmeans_folder = uf.get_files_from_folder(f"{uf.nep_location}\\Reconstruction_Phase\\Kmeans_Output", 'pkl')

# HELPER FUNCTIONS
def get_dataset_year(ds_name):
    try:
        regex = r"(?<=\-)(.*?)(?=\_)"
        year = re.findall(regex, ds_name)[0]
    except IndexError:
        year = ds_name[-4:]
    return int(year)

def load_topic_from_other_datasets(category:str, year:int, query_partisanship:str, clustering_type:str, embedding_type:str, kmeans_folder:list)->tuple:
    # Load datasets of the same topic from previous years
    # Looking at previous years bc we want to ascertain when the narratives *started* in our data
    if embedding_type:
        other_file_locs = [x for x in kmeans_folder if f"\\{query_partisanship}" not in x and embedding_type in x]
        if 'BertClusteringClassification' in other_file_locs[0]:
            if clustering_type=="0.2":
                other_file_locs = [x for x in other_file_locs if "0.3" not in x ]
            if clustering_type =="0.3":
                other_file_locs = [x for x in other_file_locs if "0.3" in x]
        else:
            other_file_locs = [x for x in other_file_locs if clustering_type in x]
    else:
        other_file_locs = [x for x in kmeans_folder if
                           f"\\{query_partisanship}" not in x and 'emoji' not in x and
                           'parentheses' not in x and 'separated' not in x]
        if 'BertClusteringClassification' in other_file_locs[0]:
            if clustering_type=="0.2":
                other_file_locs = [x for x in other_file_locs if "0.3" not in x ]
            if clustering_type =="0.3":
                other_file_locs = [x for x in other_file_locs if "0.3" in x]
        else:
            other_file_locs = [x for x in other_file_locs if clustering_type in x]
    #11111
    datasets, names = [],[] # Other files loc should be not query partisan, same cluster/ embed type
    for file in other_file_locs:
        dataset_yr = get_dataset_year(uf.get_dataset_id(file))
        if dataset_yr <= year: # if the dataset is from the same or earlier year as the query datasets,
            data = uf.import_pkl_file(file)
            try:
                datasets.append(data[category])
                names.append(file)
            except KeyError:
                continue # This happens when a topic (like Transphobia) does not appear in the keys of the dataset
    # Returns list of dataset data, list of the file names
    return datasets, names  # dataset data: keys: narratives_classified, num_clusters, cluster_centers, silhouette

def look_for_similarity_across_datasets(other_datasets:List[dict], filenames:List[str], query_centers:list):
    results = [[] for x in range(len(query_centers))]
    for d in range(len(other_datasets)): # Iterate through the other datasets
        # Get dataset info
        dataset = other_datasets[d]
        dataset_name = uf.get_dataset_id(filenames[d])
        d_centers = dataset['cluster_centers']


        for i in range(len(query_centers)): # Iterate through the cluster centers
            f_cent = query_centers[i]

            for j in range(len(d_centers)): # Iterate through the other dataset centers
                d_cent = d_centers[j]
                sim = cos(torch.from_numpy(d_cent), torch.from_numpy(f_cent))
                if float(sim) > 0.97: # if the two cluster centers are very similar:
                    if dataset_name not in results[i]:
                        results[i].append(dataset_name) # Add it to our list of results

    return results # Returns a list of size (# of clusters in query dataset) with the datasets that had matches for each

# MAIN FUNCTION
def find_unique_narratives(data, dataset_year, query_partisanship,clustering_type,embedding_type:str,kmeans_folder:list):
    results = {}
    for key in data.keys(): # Iterate through the topics
        fr_centers = data[key]['cluster_centers']

        # Get the data from previous years in the same topic
        other_datasets, filenames = load_topic_from_other_datasets(key, dataset_year, query_partisanship,
                                                                   clustering_type, embedding_type, kmeans_folder)
        matches = look_for_similarity_across_datasets(other_datasets, filenames, fr_centers)
        # Get a list of all the clusters for which there was no matching cluster in another dataset
        results[key] = [i for i in range(len(matches)) if matches[i]==[]]


    return results # Returns a dict key: topic, value: list of cluster indices that do not appear in other datasets
