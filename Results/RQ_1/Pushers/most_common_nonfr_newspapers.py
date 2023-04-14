from Results.locations import *
import universal_functions as uf
from collections import Counter



def get_unstructured_text_elts(dataset_name, article_ids):
    if dataset_name.endswith("0.2") or dataset_name.endswith("0.3"):
        dataset_name= dataset_name[:-4]
    text_loc = uf.load_files_from_prepped_datasets([f"\\{dataset_name}"])[0]
    text_data = uf.import_csv(text_loc)
    newspapers = []

    for a_id in article_ids:
        newspaper = [x[8] for x in text_data if x[0] == a_id][0]
        newspapers.append(newspaper)
    return newspapers

def find_top_fs_partisanships(fs_files, fs_mainstream_data, title):
    exportable = []
    for file in fs_files:
        fs_data = uf.import_json_content(file)
        dataset_name = uf.get_dataset_id(file)

        for topic in fs_data.keys():
            partisanships = []
            for c in fs_data[topic].keys():
                if c in fs_mainstream_data[dataset_name][topic]: # IF it has been mainstreamed
                    partisanships += [x[0] for x in fs_data[topic][c]]
            counter = Counter(partisanships).most_common(3)
            row = [dataset_name, topic]
            for tup in counter:
                row.append(tup[0])
                row.append(tup[1])
            if len(row)>2:
                exportable.append(row)
    uf.export_nested_list(f"{title}_top_fs_partisanships.csv",exportable)

def find_top_nonfr_fs(fs_files,fs_mainstream_data, kmeans_folder, title):
    newspapers = {}
    for file in fs_files:
        fs_data = uf.import_json_content(file)
        dataset_name = uf.get_dataset_id(file)
        newspapers[dataset_name] = {}
        partisanships ={}
        for topic in fs_data.keys():
            partisanships[topic] = []
            for c in fs_data[topic].keys():
                if c in fs_mainstream_data[dataset_name][topic]:  # IF it has been mainstreamed
                    ps =fs_data[topic][c]
                    for p in ps:
                        partisanships[topic].append(p)

        for t in partisanships.keys():
            publications=[]
            for file in kmeans_folder:
                kmeans_ds_name = uf.get_dataset_id(file)

                rel_clusters = [c[1] for c in partisanships[t] if c[0]==kmeans_ds_name]
                if rel_clusters == []:
                    continue

                kmeans_data = uf.import_pkl_file(file)
                art_ids = [x['article_id'] for x in kmeans_data[t]['narratives_classified'] if x['cluster_index'] in rel_clusters]

                pubs = get_unstructured_text_elts(kmeans_ds_name, art_ids)
                publications+=pubs
            newspapers[dataset_name][t]=publications

    exportable = []
    for ds in newspapers.keys():
        for t in newspapers[ds].keys():
            counter = Counter(newspapers[ds][t]).most_common(5)
            row = [ds, t]
            for tup in counter:
                row.append(tup[0])
                row.append(tup[1])
            if len(row)>2:
                exportable.append(row)
    uf.export_nested_list(f"{title}_nonfr_fs_newspapers.csv",exportable)


# find_top_fs_partisanships(fs_files=fs_97_20_nosent,fs_mainstream_data=fs_nosent_97_20_main, title="Nosent_97_2")
# find_top_fs_partisanships(fs_files=fs_97_30_nosent,fs_mainstream_data=fs_nosent_97_30_main, title="Nosent_97_3")
# find_top_fs_partisanships(fs_files=fs_98_20_nosent,fs_mainstream_data=fs_nosent_98_20_main, title="Nosent_98_2")
# find_top_fs_partisanships(fs_files=fs_98_30_nosent,fs_mainstream_data=fs_nosent_98_30_main, title="Nosent_98_3")

# find_top_nonfr_fs(fs_files=fs_97_20_nosent,fs_mainstream_data=fs_nosent_97_20_main,
#                   kmeans_folder=kmeans_97_20,title='Nosent_97_2')
# find_top_nonfr_fs(fs_files=fs_97_30_nosent,fs_mainstream_data=fs_nosent_97_30_main,
#                   kmeans_folder=kmeans_97_30,title='Nosent_97_3')
find_top_nonfr_fs(fs_files=fs_98_20_nosent,fs_mainstream_data=fs_nosent_98_20_main,
                  kmeans_folder=kmeans_98_20,title='Nosent_98_2')
find_top_nonfr_fs(fs_files=fs_98_30_nosent,fs_mainstream_data=fs_nosent_98_30_main,
                  kmeans_folder=kmeans_98_30,title='Nosent_98_3')
