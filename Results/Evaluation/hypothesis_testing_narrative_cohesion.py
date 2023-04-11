import pandas as pd
import universal_functions as uf
from statsmodels.multivariate.manova import MANOVA

# GLOBAL

results_folder_loc = uf.repo_loc / 'Results'


def get_average_internal_cohesion(data:dict)->float:
    # Input: the data from a narrative cohesion file for one dataset
    # Outputs: the average internal cohesion score of all clusters in that dataset
    cohesion = []
    for t in data.keys(): # Iterate through the topics
        for marg_cluster_id in data[t].keys(): # Iterate through the marginal cluster ids
            try:
                # Get the internal cohesion score for the marginal cluster, if it exists
                cohesion.append(float(data[t][marg_cluster_id]['cohesion']))
            except ValueError:
                continue

            # Get the direct matches of these marginal clusters
            marg_direct_matches = data[t][marg_cluster_id]['direct_matches']
            for fs_ds in marg_direct_matches.keys(): # Iterate through the direct match dataset names
                for fs_cluster_id in marg_direct_matches[fs_ds].keys(): # Iterate through the cluster ids
                    try:
                        # Get the internal cohesion score of the direct match, if it exists
                        cohesion.append(float(marg_direct_matches[fs_ds][fs_cluster_id]['internal_cohesion']))
                    except ValueError:
                        continue

                    # Get the peripheral matches of these direct matches
                    periph_matches = marg_direct_matches[fs_ds][fs_cluster_id]['periph_matches']
                    for ss_ds in periph_matches.keys():
                        for ss_cluster_id in periph_matches[ss_ds].keys():
                            cohesion.append(float(periph_matches[ss_ds][ss_cluster_id]['internal_cohesion']))
    try:
        average_cohesion = sum(cohesion)/len(cohesion)
    except ZeroDivisionError:
        average_cohesion = 0
    return average_cohesion


def get_og_dir_cohesion(data:dict)->float:
    cohesion = []

    for t in data.keys():
        for marg_cluster_id in data[t].keys():
            marg_direct_matches = data[t][marg_cluster_id]['direct_matches']
            for fs_ds in marg_direct_matches.keys():
                for fs_cluster_id in marg_direct_matches[fs_ds].keys():
                    try:
                        cohesion.append(float(marg_direct_matches[fs_ds][fs_cluster_id]['cohesion_w_og']))
                    except ValueError:
                        continue
    average_cohesion = sum(cohesion) / len(cohesion)
    return average_cohesion

def get_og_periph_cohesion(data):
    cohesion = []

    for t in data.keys():
        for marg_cluster_id in data[t].keys():


            marg_direct_matches = data[t][marg_cluster_id]['direct_matches']
            for fs_ds in marg_direct_matches.keys():
                for fs_cluster_id in marg_direct_matches[fs_ds].keys():

                    periph_matches = marg_direct_matches[fs_ds][fs_cluster_id]['periph_matches']
                    for ss_ds in periph_matches.keys():
                        for ss_cluster_id in periph_matches[ss_ds].keys():
                            try:
                                cohesion.append(float(periph_matches[ss_ds][ss_cluster_id]['cohesion_w_og']))
                            except ValueError:
                                continue
    try:
        average_cohesion = sum(cohesion) / len(cohesion)
    except ZeroDivisionError:
        average_cohesion = 0
    return average_cohesion


def get_dir_periph_cohesion(data):
    cohesion = []

    for t in data.keys():
        for marg_cluster_id in data[t].keys():

            marg_direct_matches = data[t][marg_cluster_id]['direct_matches']
            for fs_ds in marg_direct_matches.keys():
                for fs_cluster_id in marg_direct_matches[fs_ds].keys():

                    periph_matches = marg_direct_matches[fs_ds][fs_cluster_id]['periph_matches']
                    for ss_ds in periph_matches.keys():
                        try:
                            for ss_cluster_id in periph_matches[ss_ds].keys():
                                cohesion.append(float(periph_matches[ss_ds][ss_cluster_id]['cohesion_w_dir']))
                        except ValueError:
                            continue
    try:
        average_cohesion = sum(cohesion) / len(cohesion)
    except ZeroDivisionError:
        average_cohesion = 0
    return average_cohesion


def summarize_narrative_cohesion():

    # Get "narrative_cohesion" file locations
    cohesion_files = uf.get_files_from_folder(str(results_folder_loc),'json')

    # Create summary of data
    exportable = [['Pipeline','Internal_Cohesion','Og_to_Direct','Og_to_Periph','Direct_to_Periph']]
    for file in cohesion_files:

        data = uf.import_json_content(file) # import data
        pipeline = file.split('Results\\')[-1][:-24] # get the name of the pipeline

        for k in data.keys(): # Iterate through the datasets (ex: FarRight 2016)
            if 'emoji' in k:
                continue
            internal = get_average_internal_cohesion(data[k])
            og_dir = get_og_dir_cohesion(data[k])
            og_periph = get_og_periph_cohesion(data[k])
            dir_periph = get_dir_periph_cohesion(data[k])
            exportable.append([pipeline, internal, og_dir, og_periph, dir_periph])
    return exportable


# GET DATA
data = summarize_narrative_cohesion() # Summarize the data from the narrative cohesion files
df = pd.DataFrame(data=data[1:], columns=data[0]) # Create a dataframe

# MANOVA TEST
fit = MANOVA.from_formula('Internal_Cohesion + Og_to_Direct + Og_to_Periph + Direct_to_Periph ~ Pipeline', data=df)
print(fit.mv_test())