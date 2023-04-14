import universal_functions as uf
from Results.locations import *

all_narr = all_narr_97_20 + all_narr_97_30 + all_narr_98_20 + all_narr_98_30
direct_files = dir_narr_97_20 + dir_narr_97_30 + dir_narr_98_20 + dir_narr_98_30
periph_files = periph_narr_97_20 + periph_narr_97_30 +periph_narr_98_20 +periph_narr_98_30
kmeans_files = kmeans_97_20 + kmeans_97_30 + kmeans_98_20 + kmeans_98_30
reduced_files = [x for x in uf.get_files_from_folder(f"{uf.thesis_location}locally_createEmbeddings\\Reduced_SROs","json") if 'Sentiment' in x]

def get_class_cluster_type(dataset_name):
    split_ = dataset_name.split("_")
    if len(split_)==4:
        cluster_type = split_[2]
        class_type  =split_[3]
        ds_name = f"{split_[0]}_{split_[1]}"
    else:
        cluster_type = split_[3]
        class_type = split_[4]
        ds_name = f"{split_[0]}_{split_[1]}"
    return ds_name, class_type, cluster_type

def get_dataset_id(filename, dataset_name):
    if "0.2" in filename:
        cluster_type = "0.2"
    else:
        cluster_type = "0.3"
    if "Low" in filename:
        class_type = "97"
    else:
        class_type = "98"
    return f"{dataset_name}_{cluster_type}_{class_type}"


def get_dataset_clusters(dataset_name):
    marg_files = [x for x in all_narr if f"\\{dataset_name}" in x]
    dir_files = [x for x in direct_files if f"\\{dataset_name}" in x]
    peripheral_files = [x for x in periph_files if f"\\{dataset_name}" in x]

    dataset_clusters = {}
    for m_file in marg_files:
        m_data = uf.import_json_content(m_file)

        for k in m_data.keys():
            m_dataset_id =get_dataset_id(m_file,k)
            if m_dataset_id not in dataset_clusters.keys():
                dataset_clusters[m_dataset_id] = []
            for t in m_data[k].keys():
                for m_cluster_id in m_data[k][t].keys():
                    dataset_clusters[m_dataset_id].append([t, m_cluster_id])

    for d_file in dir_files:
        d_data = uf.import_json_content(d_file)
        for k in d_data.keys():
            for t in d_data[k].keys():
                for marg_cluster_id in d_data[k][t].keys():
                    for fs_ds in d_data[k][t][marg_cluster_id].keys():
                        d_dataset_id = get_dataset_id(d_file, fs_ds)
                        if d_dataset_id not in dataset_clusters.keys():
                            dataset_clusters[d_dataset_id] = []
                        for fs_cluster_id in d_data[k][t][marg_cluster_id][fs_ds].keys():
                            dataset_clusters[d_dataset_id].append([t, fs_cluster_id])

    for p_file in peripheral_files:
        p_data = uf.import_json_content(p_file)
        for k in p_data.keys():
            for t in p_data[k].keys():
                for marg_cluster_id in p_data[k][t].keys():
                    for fs_ds in p_data[k][t][marg_cluster_id].keys():
                        for fs_cluster_id in p_data[k][t][marg_cluster_id][fs_ds].keys():
                            for ss_ds in p_data[k][t][marg_cluster_id][fs_ds][fs_cluster_id].keys():
                                p_dataset_id = get_dataset_id(p_file, ss_ds)
                                if p_dataset_id not in dataset_clusters.keys():
                                    dataset_clusters[p_dataset_id] = []
                                for ss_cluster_id in p_data[k][t][marg_cluster_id][fs_ds][fs_cluster_id][ss_ds]:
                                    dataset_clusters[p_dataset_id].append([t, ss_cluster_id])
    return dataset_clusters

def get_dataset_elements(dataset, cluster_ids, kmeans_folder):
    kmeans_loc = [x for x in kmeans_folder if f"\\{dataset}" in x]
    kmeans_data = uf.import_pkl_file(kmeans_loc[0])

    cluster_elts = []
    for c in cluster_ids:
        cluster_elts += [x for x in kmeans_data[c[0]]['narratives_classified'] if str(x['cluster_index'])==c[1]]
    return cluster_elts


def get_rel_triplets(file):
    kmeans_conversion = {'97':{"0.2":kmeans_97_20,
                               "0.3":kmeans_97_30},
                         '98':{"0.2":kmeans_98_20,
                               "0.3":kmeans_98_30}}
    dataset_name = uf.get_dataset_id(file)
    dataset_clusters = get_dataset_clusters(dataset_name)

    dataset_elts = {}
    for k in dataset_clusters:
        ds_name, class_type, cluster_type = get_class_cluster_type(k)
        kmeans_folder = kmeans_conversion[class_type][cluster_type]
        dataset_elts[k]=get_dataset_elements(ds_name, dataset_clusters[k], kmeans_folder)

    for k in dataset_elts.keys():
        ds_name, class_type, cluster_type = get_class_cluster_type(k)
        # check if this processs has already been done
        # check if there is a reduced file
        reduced_file = [x for x in reduced_files if f"\\{dataset_name}" in x]
        if len(reduced_file)>0:
            if "checkpoint" not in file:
                print('-- sent data already exists --')
            reduced_data = uf.import_json_content(reduced_file[0])


        # check if there is a complete file



# For a given SRO file, get all relevant triplets
sro_files = [x for x in uf.load_all_complete_datasets() if "FarRight" in x]
for file in sro_files:
    get_rel_triplets(file)
