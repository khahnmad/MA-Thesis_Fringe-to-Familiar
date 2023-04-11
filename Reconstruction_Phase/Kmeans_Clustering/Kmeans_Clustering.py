import universal_functions as uf
from sklearn.cluster import KMeans
import numpy as np
import re
import sklearn
from typing import List

# GLOBAL
high_cosine_loc = uf.repo_loc / 'Reconstruction_Phase/Cosine_Matching_Classification/output/high'
high_cosine_folder = uf.get_files_from_folder(str(high_cosine_loc),'pkl')
low_cosine_loc = uf.repo_loc / 'Reconstruction_Phase/Cosine_Matching_Classification/output/low'
lowclass_cosine_folder = uf.get_files_from_folder(str(low_cosine_loc),"pkl")
kmeans_output= uf.repo_loc / 'Kmeans_Clustering/output'


def do_kmeans_clustering(category:list, n_percent)->tuple:
    n = int(n_percent*len(category)) # TODO
    embeddings = [np.array(x['embedding']) for x in category if x['embedding']!=None]
    # TODO: Have to optimize/ evaluate to know what n works best
    cluster = KMeans(n_clusters=n, random_state=0).fit(embeddings)
    cluster_centers = list(cluster.cluster_centers_)
    silhouette_score = sklearn.metrics.silhouette_score(
        X=embeddings,
        labels=cluster.labels_)
    # Returns the kmeans object, the # of clusters the cluster centers, & silhouette score
    return cluster,n, cluster_centers, silhouette_score


def save_narrative_clusters(kmeans_cluster, category:List[dict])-> List[dict]: # kmeans object, list of data
    """
    Goal: index for each cluster, add that to the existing object ie obj.cluster_indices = {'Immigration':1}
    then export the data
    """
    for i in range(len(category)):
        category[i]['cluster_index'] = list(kmeans_cluster.labels_)[i]
    return category # Returns a list of all elts with the new k,v pair "cluster_index" : int


def get_checkpoint(file):
    if 'EmbCOMPLETE'.lower() not in file.lower():
        if "Kmeans" in file:
            regex = r"(?<=Emb)(.*?)(?=\_)"
            checkpoint = int(re.findall(regex, file)[0])
            return checkpoint
        elif 'CosineMatching.pkl' in file:
            regex = r"(?<=Emb)(.*?)(?=\_Cosine)"
            checkpoint = int(re.findall(regex, file)[0])
            return checkpoint
        elif 'checkpoint' in file:
            regex = r"(?<=Emb)(.*?)(?=\_checkpoint)"
            checkpoint = int(re.findall(regex, file)[0])
            return checkpoint
        else:
            regex = r"(?<=Emb)(.*?)(?=\.)"
            checkpoint = int(re.findall(regex, file)[0])
            return checkpoint
    return 'COMPLETE'


def find_narratives(file, n_percent, export_name):
    data = uf.import_pkl_file(file)
    if 'checkpoint' in file:
        data = data['sorted_dict']


    narratives = {}
    for cat in data.keys():
        if len(data[cat]) < 10:
            continue
        clusters, n, centers, silhouette = do_kmeans_clustering(data[cat], n_percent)
        data[cat] = [x for x in data[cat] if x['embedding']!=None] # Remove the none embeddings
        n_clusters = save_narrative_clusters(clusters, data[cat])

        narratives[cat] = {"narratives_classified": n_clusters,
                           "num_clusters":n,
                           "cluster_centers":centers,
                           'silhoutte':silhouette}

    print("    Exporting ...")
    uf.export_as_pkl(export_name=export_name, content=narratives)


def already_run(filename:str,n_percent)->bool:
    dataset_name = uf.get_dataset_id(filename)
    emb_checkpoint = get_checkpoint(filename)
    export_name = str(kmeans_output) +f"{dataset_name}_{n_percent}_Emb{emb_checkpoint}.pkl"
    prev_files = uf.get_files_from_folder(str(kmeans_output),"pkl")
    if export_name in prev_files:
        return True
    return False

def run_higher_classification_kmeans(threshold):
    for file in high_cosine_folder[40:]:
        print(f"\nRunning {file}")

        emb_checkpoint = get_checkpoint(file)
        dataset_name = uf.get_dataset_id(file)
        export_name = str(kmeans_output)+f"{dataset_name}_{threshold}_Emb{emb_checkpoint}_Kmeans.pkl"

        exists = already_run(file,n_percent)
        if exists ==True:
            print(f"-- already run --")
            continue

        find_narratives(file, threshold, export_name)

def run_lower_classification_kmeans(threshold):
    for file in lowclass_cosine_folder[39:]:
        emb_checkpoint = get_checkpoint(file)
        dataset_name = uf.get_dataset_id(file)
        print(f"Running {dataset_name}...")
        if threshold == 0.3:
            # export_folder = f"{uf.nep_location}BertClusteringCLassification\\KmeansOutput\\Diff_percent\\"
            export_name = str(kmeans_output) + f"{dataset_name}_Emb{emb_checkpoint}_Kmeans_0.3.pkl"
            kmeans_folder = uf.get_files_from_folder(str(kmeans_output),'pkl')
        else:
            # export_folder = f"{uf.nep_location}BertClusteringCLassification\\KmeansOutput\\"
            export_name = str(kmeans_output) + f"{dataset_name}_Emb{emb_checkpoint}_Kmeans.pkl"
            kmeans_folder = uf.get_files_from_folder(str(kmeans_output),'pkl')

        if export_name in kmeans_folder:
            print("    -- Already Complete --")
            continue

        find_narratives(file, threshold, export_name=export_name)


if __name__ == '__main__':
    n_percent = 0.3


    # run_lower_classification_kmeans(n_percent)

    run_higher_classification_kmeans(n_percent)
