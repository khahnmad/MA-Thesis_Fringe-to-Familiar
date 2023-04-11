import universal_functions as uf
from Results.config.locations import *
import random


def get_cluster_text(dataset_name, topic, cluster_id, kmeans_folder):
    kmeans_loc = [x for x in kmeans_folder if f"\\{dataset_name}" in x]
    kmeans_data = uf.import_pkl_file(kmeans_loc[0])

    cluster_elts = [x for x in kmeans_data[topic]['narratives_classified'] if x['cluster_index']==int(cluster_id)]
    text = [f"{elt['subject']} {elt['relation']} {elt['object']}" for elt in cluster_elts]
    return text


def evaluate_narrative_cohesion(class_type:str, cluster_type:str, kmeans_folder:list):
    direct_files = [x for x in uf.get_files_from_folder(f"{uf.thesis_location}Tracking\\{class_type}Class_Threshold\\","json")
                    if "direct" in x and cluster_type in x]
    export_name = f'{class_type}_{cluster_type}_Narrative_Cohesion.json'
    try:
        results = uf.import_json_content(export_name)
    except FileNotFoundError:
        results ={}
    for file in direct_files:
        data = uf.import_json_content(file)
        for k in data.keys():
            if k not in results.keys():
                results[k] = {}

            for t in data[k].keys():
                if t not in results[k].keys():
                    results[k][t] = {}
                else:
                    continue

                for marg_cluster_id in data[k][t].keys():
                    if marg_cluster_id not in results[k][t].keys():
                        results[k][t][marg_cluster_id] = {'label':'',
                                                          'cohesion':'',
                                                          'direct_matches':{}}
                    else:
                        continue
                    marg_text = get_cluster_text(k,t,marg_cluster_id, kmeans_folder)
                    print("Marginal Text:")
                    for m in marg_text:
                        print(f"    {m}")
                    m_label = input("Label:")
                    m_cohesion = input('Cohesion (-1/0/1):')

                    results[k][t][marg_cluster_id]['label'] = m_label
                    results[k][t][marg_cluster_id]['cohesion'] = m_cohesion
                    uf.content_json_export(export_name, results)

                    for fs_ds in data[k][t][marg_cluster_id].keys():
                        if fs_ds not in results[k][t][marg_cluster_id]['direct_matches'].keys():
                            results[k][t][marg_cluster_id]['direct_matches'][fs_ds] = {}

                        for fs_cluster_id in data[k][t][marg_cluster_id][fs_ds].keys():
                            if fs_cluster_id not in results[k][t][marg_cluster_id]['direct_matches'][fs_ds].keys():
                                results[k][t][marg_cluster_id]['direct_matches'][fs_ds][fs_cluster_id] = {'label':'',
                                                                                                          'internal_cohesion':'',
                                                                                                          'cohesion_w_og':'',
                                                                                                          'periph_matches':{}}
                            fs_cluster_text = get_cluster_text(fs_ds,t,fs_cluster_id,kmeans_folder)
                            print(f"\nDirect Match Text:")
                            for f in fs_cluster_text:
                                print(f"    {f}")
                            f_label = input("Label:")
                            f_cohesion = input('Internal Cohesion (-1/0/1):')
                            f_marg_cohesion = input('Cohesion with Og narrative (-1/0/1):')

                            results[k][t][marg_cluster_id]['direct_matches'][fs_ds][fs_cluster_id]['label'] = f_label
                            results[k][t][marg_cluster_id]['direct_matches'][fs_ds][fs_cluster_id]['internal_cohesion'] = f_cohesion
                            results[k][t][marg_cluster_id]['direct_matches'][fs_ds][fs_cluster_id]['cohesion_w_og'] = f_marg_cohesion
                            uf.content_json_export(export_name,results)

                            for ss_ds in data[k][t][marg_cluster_id][fs_ds][fs_cluster_id].keys():
                                if ss_ds not in results[k][t][marg_cluster_id]['direct_matches'][fs_ds][fs_cluster_id]['periph_matches'].keys():
                                    results[k][t][marg_cluster_id]['direct_matches'][fs_ds][fs_cluster_id][
                                        'periph_matches'][ss_ds] ={}

                                num_samples = min(len(data[k][t][marg_cluster_id][fs_ds][fs_cluster_id][ss_ds]), 5)
                                periph_text = []
                                for i in range(num_samples):
                                    rand_ss_cluster_id_index = random.randint(0,len(data[k][t][marg_cluster_id][fs_ds][fs_cluster_id][ss_ds])-1)
                                    ss_cluster_id = data[k][t][marg_cluster_id][fs_ds][fs_cluster_id][ss_ds][rand_ss_cluster_id_index]

                                    if ss_cluster_id not in results[k][t][marg_cluster_id]['direct_matches'][fs_ds][fs_cluster_id][
                                        'periph_matches'][ss_ds].keys():
                                        results[k][t][marg_cluster_id]['direct_matches'][fs_ds][fs_cluster_id][
                                            'periph_matches'][ss_ds][ss_cluster_id] = {}

                                        periph_text = get_cluster_text(ss_ds,t,ss_cluster_id,kmeans_folder)

                                        print(f"\nPeriph Match Text:")
                                        for p in periph_text:
                                            print(f"    {p}")
                                        p_label = input("Label:")
                                        p_cohesion = input('Internal Cohesion (-1/0/1):')
                                        p_marg_cohesion = input('Cohesion with Og narrative (-1/0/1):')
                                        p_dir_cohesion = input('Cohesion with Direct narrative (-1/0/1):')

                                        results[k][t][marg_cluster_id]['direct_matches'][fs_ds][fs_cluster_id][
                                            'periph_matches'][ss_ds][ss_cluster_id]['label'] = p_label
                                        results[k][t][marg_cluster_id]['direct_matches'][fs_ds][fs_cluster_id][
                                            'periph_matches'][ss_ds][ss_cluster_id][
                                            'internal_cohesion'] = p_cohesion
                                        results[k][t][marg_cluster_id]['direct_matches'][fs_ds][fs_cluster_id][
                                            'periph_matches'][ss_ds][ss_cluster_id][
                                            'cohesion_w_og'] = p_marg_cohesion
                                        results[k][t][marg_cluster_id]['direct_matches'][fs_ds][fs_cluster_id][
                                            'periph_matches'][ss_ds][ss_cluster_id][
                                            'cohesion_w_dir'] = p_dir_cohesion
                                        uf.content_json_export(export_name, results)


def summarize_narrative_cohesion():
    cohesion_files = uf.get_files_from_folder(f"{uf.thesis_location}Results",'json')
    exportable = [['Pipeline','Internal Cohesion','Og to Direct','Og to Periph','Direct to Periph']]
    for file in cohesion_files:
        data = uf.import_json_content(file)
        pipeline = file.split('Results\\')[-1][:-24]

        internal = get_average_internal_cohesion(data)
        og_dir = get_og_dir_cohesion(data)
        og_periph = get_og_periph_cohesion(data)
        dir_periph = get_dir_periph_cohesion(data)
        exportable.append([pipeline, internal, og_dir, og_periph, dir_periph])
    uf.export_nested_list('Summarized_Narrative_Cohesion.csv',exportable)


def get_average_internal_cohesion(data):
    cohesion = []
    for k in data.keys():
        for t in data[k].keys():
            for marg_cluster_id in data[k][t].keys():
                try:
                    cohesion.append(float(data[k][t][marg_cluster_id]['cohesion']))
                except ValueError:
                    continue

                marg_direct_matches = data[k][t][marg_cluster_id]['direct_matches']
                for fs_ds in marg_direct_matches.keys():
                    for fs_cluster_id in marg_direct_matches[fs_ds].keys():
                        try:
                            cohesion.append(float(marg_direct_matches[fs_ds][fs_cluster_id]['internal_cohesion']))
                        except ValueError:
                            continue

                        periph_matches = marg_direct_matches[fs_ds][fs_cluster_id]['periph_matches']
                        for ss_ds in periph_matches.keys():
                            for ss_cluster_id in periph_matches[ss_ds].keys():
                                cohesion.append(float(periph_matches[ss_ds][ss_cluster_id]['internal_cohesion']))
    average_cohesion = sum(cohesion)/len(cohesion)
    return average_cohesion

def get_og_dir_cohesion(data):
    cohesion = []
    for k in data.keys():
        for t in data[k].keys():
            for marg_cluster_id in data[k][t].keys():
                marg_direct_matches = data[k][t][marg_cluster_id]['direct_matches']
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
    for k in data.keys():
        for t in data[k].keys():
            for marg_cluster_id in data[k][t].keys():


                marg_direct_matches = data[k][t][marg_cluster_id]['direct_matches']
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
    for k in data.keys():
        for t in data[k].keys():
            for marg_cluster_id in data[k][t].keys():

                marg_direct_matches = data[k][t][marg_cluster_id]['direct_matches']
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



if __name__ == '__main__':

    summarize_narrative_cohesion()

    # Run narrative cohesion
    for class_type in ["High","Low"]:
        for cluster_type in ["0.2","0.3"]:
            if class_type == "Low":
                if cluster_type == "0.2":
                    kmeans_folder = kmeans_97_20
                else:
                    kmeans_folder = kmeans_97_30
            else:
                if cluster_type == "0.2":
                    kmeans_folder = kmeans_98_20
                else:
                    kmeans_folder = kmeans_98_30
            evaluate_narrative_cohesion(class_type, cluster_type, kmeans_folder)