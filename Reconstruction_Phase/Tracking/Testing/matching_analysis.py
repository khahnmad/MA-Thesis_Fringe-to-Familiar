from Tracking.Pipeline.StarterNarrative_Identification import get_dataset_year, look_for_similarity_across_datasets
from Tracking.Pipeline.generalized_two_step_tracking import get_embedding_type
import universal_functions as uf
from Results.locations import *
from collections import Counter

# key is to find marginal narratives that do have mathces
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


def find_narrative_matches(data,dataset_year, query_partisanship, clustering_type, embedding_type, kmeans_folder):
    matches = {}
    for key in data.keys():  # Iterate through the topics
        fr_centers = data[key]['cluster_centers']

        # Get the data from previous years in the same topic
        other_datasets, filenames = load_topic_from_other_datasets(key, dataset_year, query_partisanship,
                                                                   clustering_type, embedding_type, kmeans_folder)
        topic_matches= look_for_similarity_across_datasets(other_datasets, filenames, fr_centers)
        counter = Counter(uf.flatten_list(topic_matches)).most_common(5)
        matches[key] = counter
    return matches


# MAIN
# p= "FarRight"
# kmeans_folder = kmeans_97_20+kmeans_97_30
# part_kmeans_files = [x for x in kmeans_folder if f"\\{p}_" in x]
# results = {}
# for file in part_kmeans_files:
#
#     dataset_name = uf.get_dataset_id(file)
#
#     dataset_year = get_dataset_year(dataset_name)
#     # cluster_type = dataset_name[-3:]
#     if "Diff_percent" in file:
#         cluster_type = "0.3"  # 11
#     else:
#         cluster_type = "0.2"  # 11111
#     embed_type = get_embedding_type(year=dataset_year, cluster_type=cluster_type, ds_name=dataset_name)
#     if embed_type:
#         continue
#     kmeans_data = uf.import_pkl_file(file)
#     print(f"    On year: {dataset_year}...")
#
#     # Run the file
#     common_matches = find_narrative_matches(data=kmeans_data, dataset_year=dataset_year,
#                                                    query_partisanship=p, clustering_type=cluster_type,
#                                                    embedding_type=embed_type,kmeans_folder=kmeans_folder)
#     results[f"{dataset_name}_{cluster_type}"] = common_matches
#
# uf.content_json_export("97_common_matches.json",results)

def common_matches_98():
    p = "FarRight"
    kmeans_folder = kmeans_98_20 + kmeans_98_30
    part_kmeans_files = [x for x in kmeans_folder if f"\\{p}_" in x]
    results = {}
    for file in part_kmeans_files:

        dataset_name = uf.get_dataset_id(file)

        dataset_year = get_dataset_year(dataset_name)
        cluster_type = dataset_name[-3:]
        embed_type = get_embedding_type(year=dataset_year, cluster_type=cluster_type, ds_name=dataset_name)
        if embed_type:
            continue
        kmeans_data = uf.import_pkl_file(file)
        print(f"    On year: {dataset_year}...")

        # Run the file
        common_matches = find_narrative_matches(data=kmeans_data, dataset_year=dataset_year,
                                                query_partisanship=p, clustering_type=cluster_type,
                                                embedding_type=embed_type, kmeans_folder=kmeans_folder)
        results[f"{dataset_name}_{cluster_type}"] = common_matches

    uf.content_json_export("98_common_matches.json", results)

# common_matches_98()

uf.im