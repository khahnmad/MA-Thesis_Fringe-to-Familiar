"""
This script identifies marginal narratives among the Far Right datasets and then identifies matches to these marginal
narratives in the direct and peripheral steps. It accounts for both a cosine classification threshold of 0.97 and 0.985
and a cluster number of 0.2 and 0.3
"""
import universal_functions as uf
from Reconstruction_Phase.Tracking.Pipeline import direct_matching as dm, peripheral_matching as pm, marginal_narrative_identification as mi

import json
import re

# GLOBAL

# Kmeans files
kmeans_folder_loc = uf.repo_loc / 'Reconstruction_Phase/Kmeans_Clustering/output'
kmeans_folder_97 = uf.get_files_from_folder(str(kmeans_folder_loc / 'threshold_97'),"pkl")
kmeans_folder_98 = uf.get_files_from_folder(str(kmeans_folder_loc / 'threshold_985'),'pkl')

# Tracking files
tracking_folder = uf.repo_loc / 'Reconstruction_Phase/Tracking'

un_folder_98_loc = tracking_folder / 'HighClass_Threshold/Marginal_Narratives'
un_folder_97_loc = tracking_folder / 'LowClass_Threshold/Marginal_Narratives'

dm_folder_98_loc = 'HighClass_Threshold/Direct_Matches'
dm_folder_97_loc = 'HighClass_Threshold/Direct_Matches'

pm_folder_98_loc = tracking_folder / 'HighClass_Threshold/Peripheral_Matches'
pm_folder_97_loc = tracking_folder / 'LowClass_Threshold/Peripheral_Matches'


# HELPER FUNCTIONS
def get_dataset_year(ds_name:str)->int:
    # Extract the year of the dataset from the filename
    try:
        regex = r"(?<=\-)(.*?)(?=\_)"
        year = re.findall(regex, ds_name)[0]
    except IndexError:
        year = ds_name.split('-')[-1]
    return int(year) # 11111


def get_embedding_type(year, cluster_type, ds_name):
    try:
        regex = fr"(?<={year})(.*?)(?={cluster_type})"
        match = re.findall(regex, ds_name)[0]
        if match != "_":
            return match[1:-1]
        return None # 1111
    except IndexError:
        if str(year) == ds_name[-4:]:
            return None # 11111
        embedding_type = ds_name.split('_')[-1]
        return embedding_type # 111


def file_has_been_run(dataset_name:str, ss_loc:str)->bool:
    if f"{ss_loc}\\{dataset_name}.json" in uf.get_files_from_folder(ss_loc,"json"):
        return True # 11111
    return False # 11111


def starter_has_been_run(ds_name:str, un_loc:str)->bool:
    if f"{un_loc}\\{ds_name}.json" in uf.get_files_from_folder(un_loc,"json"):
        return True # 1111
    return False # 11111


def first_step_has_been_run(ds_name:str, fs_loc:str)->bool:
    if f"{fs_loc}\\{ds_name}.json" in uf.get_files_from_folder(fs_loc,"json"):
        return True #1111
    return False # 1111


def track_narratives(kmeans_folder:list, un_folder:str, dm_folder:str, pm_folder:str):
    for p in ['FarRight']: # HERE can introduce tracking starting with other partisanships
        part_kmeans_files = [x for x in kmeans_folder if f"\\{p}_" in x]

        print(f"\nRunning {p}, found {len(part_kmeans_files)} Kmeans files...")
        for file in part_kmeans_files: # 1
            # Get necessary data
            dataset_name = uf.get_dataset_id(file)
            dataset_year = get_dataset_year(dataset_name)
            cluster_type = dataset_name[-3:]

            if cluster_type not in dataset_name:
                for_file_run = f"{dataset_name}_{cluster_type}"
            else:
                for_file_run = dataset_name

            print(f"    Running {dataset_name}, {dataset_year}, {cluster_type}")
            if file_has_been_run(for_file_run,pm_folder ) ==True:
                print(f"    -- SKIPPING, file is already complete --")
                continue

            embed_type = get_embedding_type(year=dataset_year, cluster_type=cluster_type, ds_name=dataset_name)
            if embed_type:
                print(f"    -- skipping embedding type '{embed_type}' -- ")
                continue

            kmeans_data = uf.import_pkl_file(file)

            # Run the file
            starter_export_name = f"{un_folder}\\{dataset_name}_{cluster_type}.json"
            if starter_has_been_run(for_file_run, un_folder) == True:
                starter_narratives = uf.import_json_content(starter_export_name)
                print(f"       -- loading marginal narratives --")
            else:
                starter_narratives = mi.find_unique_narratives(data=kmeans_data,
                                                               dataset_year=dataset_year,
                                                               query_partisanship=p,
                                                               clustering_type=cluster_type,
                                                               embedding_type=embed_type,
                                                               kmeans_folder=kmeans_folder)
                print(f"       -- exporting marginal narratives --")
                starter_export = json.dumps({'content': starter_narratives})
                uf.export_as_json(starter_export_name, starter_export)
                # ^ Returns a dict key: topic, value: list of cluster indices that do not appear in other datasets

            first_step_export_name = f"{dm_folder}\\{dataset_name}_{cluster_type}.json"
            if first_step_has_been_run(for_file_run, dm_folder) == True:
                first_step = uf.import_json_content(first_step_export_name)
                print(f"       -- loading direct match narratives --")
            else:
                first_step = dm.run_first_step_tracking(starter_narratives=starter_narratives,
                                                        dataset_name=dataset_name,
                                                        dataset_year=dataset_year,
                                                        kmeans_folder=kmeans_folder,
                                                        clustering_type=cluster_type,
                                                        embedding_type=embed_type)
                print(f"       -- exporting direct match narratives --")
                uf.content_json_export(export_name=first_step_export_name,
                                       data=first_step)


            second_step = pm.run_second_step_tracking(first_step, kmeans_folder, cluster_type, embed_type)
            print(f"       -- exporting peripheral match narratives --")
            second_export = json.dumps({'content': second_step})
            second_exportname = f"{pm_folder}\\{dataset_name}_{cluster_type}.json"
            uf.export_as_json(second_exportname, second_export)

def track_low_threshold():
    print("Tracking Low Threshold Narratives...")
    track_narratives(kmeans_folder_97, un_folder_97_loc, dm_folder_97_loc, pm_folder_97_loc)


def track_high_threshold():
    print("Tracking High Threshold Narratives...")
    track_narratives(kmeans_folder_98, un_folder_98_loc, dm_folder_98_loc, pm_folder_98_loc)


# MAIN FUNCTION
if __name__ == '__main__':
    track_low_threshold()
    track_high_threshold()