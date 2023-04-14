import universal_functions as uf
from Results.locations import *

def get_NEs(cluster_ids, kmeans, dataset_name, topic):
    kmeans_loc = [x for x in kmeans if f"\\{dataset_name}" in x][0]
    kmeans_data = uf.import_pkl_file(kmeans_loc)
    types = ["NATIONALITY","PERSON","MISC","COUNTRY","RELIGION","ORGANIZATION","TITLE","STATE_OR_PROVINCE"]
    NEs = []
    for cluster_id in cluster_ids:
        cluster_elts = [x['entity_location'] for x in kmeans_data[topic]['narratives_classified'] if x['cluster_index'] == int(cluster_id)]
        for elt in cluster_elts:
            if len(elt)<1:
                continue
            for k in elt.keys():
                for item in elt[k]:
                    if item["ner"] in types:
                        NEs.append([item['text'], item['ner'],k])

    return NEs

def get_NEs_marg_narratives(marg_narr_loc, kmeans_folder, export_name):
    data = uf.import_json_content(marg_narr_loc)
    ds_name = uf.get_dataset_id(marg_narr_loc)
    if '0.2' in marg_narr_loc:
        cluster_type = "0.2"
    else:
        cluster_type = "0.3"
    marg_nes = {}
    for k in data.keys():
        marg_nes[k]={}
        for t in data[k].keys():
            marg_nes[k][t] ={}
            for marg_cluster_id in data[k][t].keys():
                entities = get_NEs([marg_cluster_id],kmeans=kmeans_folder, dataset_name=k, topic=t)
                marg_nes[k][t][marg_cluster_id]=entities
    export_name = f"{export_name}{ds_name}_{cluster_type}_marginal_NEs.json"
    uf.content_json_export(export_name,marg_nes)

def get_NEs_direct(direct_narr_loc, kmeans_folder, export_name):
    data = uf.import_json_content(direct_narr_loc)
    ds_name = uf.get_dataset_id(direct_narr_loc)
    if '0.2' in direct_narr_loc:
        cluster_type = "0.2"
    else:
        cluster_type = "0.3"

    direct_nes = {}
    for k in data.keys():
        direct_nes[k] = {}
        for t in data[k].keys():
            direct_nes[k][t] = {}
            for marg_cluster_id in data[k][t].keys():
                direct_nes[k][t][marg_cluster_id] = {}
                for fs_ds in data[k][t][marg_cluster_id].keys():
                    direct_nes[k][t][marg_cluster_id][fs_ds] = {}
                    for fs_cluster_id in data[k][t][marg_cluster_id][fs_ds].keys():
                        entities = get_NEs([fs_cluster_id], kmeans=kmeans_folder, dataset_name=fs_ds, topic=t)
                        direct_nes[k][t][marg_cluster_id][fs_ds][fs_cluster_id] = entities
    export_name = f"{export_name}{ds_name}_{cluster_type}_direct_NEs.json"
    uf.content_json_export(export_name, direct_nes)

def run_all_marg_narratives(marg_narr, kmeans, title):
    for file in marg_narr:
        export_loc = f"{uf.thesis_location}Results\\rq_2\\no_sent\\{title}\\"
        get_NEs_marg_narratives(file, kmeans, export_loc)


def run_all_direct(direct_folder,kmeans, title):
    for file in direct_folder:
        export_loc = f"{uf.thesis_location}Results\\rq_2\\no_sent\\{title}\\"
        get_NEs_direct(file, kmeans, export_loc)


def run_all_periph(periph_folder, kmeans, title):
    for file in periph_folder:
        export_loc = f"{uf.thesis_location}Results\\rq_2\\no_sent\\{title}\\"
        get_NEs_periph(file, kmeans, export_loc)

def get_NEs_periph(file, kmeans_folder, export_loc):
    data = uf.import_json_content(file)
    ds_name = uf.get_dataset_id(file)
    if '0.2' in file:
        cluster_type = "0.2"
    else:
        cluster_type = "0.3"

    periph_nes = {}
    for k in data.keys():
        periph_nes[k] = {}
        for t in data[k].keys():
            periph_nes[k][t] = {}
            for marg_cluster_id in data[k][t].keys():
                periph_nes[k][t][marg_cluster_id] = {}
                for fs_ds in data[k][t][marg_cluster_id].keys():
                    periph_nes[k][t][marg_cluster_id][fs_ds] = {}
                    for fs_cluster_id in data[k][t][marg_cluster_id][fs_ds].keys():
                        periph_nes[k][t][marg_cluster_id][fs_ds][fs_cluster_id] = {}
                        for ss_ds in data[k][t][marg_cluster_id][fs_ds][fs_cluster_id].keys():
                            periph_nes[k][t][marg_cluster_id][fs_ds][fs_cluster_id][ss_ds] =[]
                            for ss_cluster_id in data[k][t][marg_cluster_id][fs_ds][fs_cluster_id][ss_ds]:
                                entities = get_NEs([ss_cluster_id], kmeans=kmeans_folder, dataset_name=fs_ds, topic=t)
                                periph_nes[k][t][marg_cluster_id][fs_ds][fs_cluster_id][ss_ds].append(entities)
    export_name = f"{export_loc}{ds_name}_{cluster_type}_periph_NEs.json"
    uf.content_json_export(export_name, periph_nes)



# run_all_marg_narratives(all_narr_97_20, kmeans_97_20, 'cosine_97')
# run_all_marg_narratives(all_narr_97_30, kmeans_97_30, 'cosine_97')

# run_all_direct(dir_narr_97_20, kmeans_97_20, 'cosine_97')
# run_all_direct(dir_narr_97_30, kmeans_97_30, 'cosine_97')
#
# run_all_periph(periph_narr_97_20, kmeans_97_20, 'cosine_97')
# run_all_periph(periph_narr_97_30, kmeans_97_30, 'cosine_97')

run_all_marg_narratives(all_narr_98_20, kmeans_98_20, 'cosine_98')
run_all_marg_narratives(all_narr_98_30, kmeans_98_30, 'cosine_98')

run_all_direct(dir_narr_98_20, kmeans_98_20, 'cosine_98')
run_all_direct(dir_narr_98_30, kmeans_98_30, 'cosine_98')

run_all_periph(periph_narr_98_20, kmeans_98_20, 'cosine_98')
run_all_periph(periph_narr_98_30, kmeans_98_30, 'cosine_98')