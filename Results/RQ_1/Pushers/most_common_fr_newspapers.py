"""
Find top Far Right newspapers in marginal narratives, first step mainstreamed, second mainstreamed
"""
from Results.locations import *
import universal_functions as uf
from collections import Counter

def collect_article_ids(data, kmeans_data):
    article_ids = {topic: {} for topic in data.keys()}
    for t in data.keys():
        for cluster_id in data[t]:
            cluster_elts = [x['article_id'] for x in kmeans_data[t]['narratives_classified'] if
                            x['cluster_index'] == int(cluster_id)]
            article_ids[t][cluster_id] = cluster_elts
    return article_ids


def get_unstructured_text_elts(dataset_name, article_ids):
    text_loc = uf.load_files_from_prepped_datasets([dataset_name])[0]
    text_data = uf.import_csv(text_loc)
    newspapers = {topic: {} for topic in article_ids.keys()}
    for t in article_ids.keys():
        for c in article_ids[t]:
            newspapers[t][c] = []
            for a_id in article_ids[t][c]:
                newspaper = [x[8] for x in text_data if x[0] == a_id][0]
                newspapers[t][c].append(newspaper)
    return newspapers


def find_top_marginal_newspapers(marginal_files:list, kmeans_folder:list, title:str):
    marginal_newspapers = {}
    for loc in marginal_files:
        # Get marginal narratives
        marginal_data = uf.import_json_content(loc)
        dataset_name = uf.get_dataset_id(loc)

        # Get corresponding kmeans clustering
        kmeans_loc = [x for x in kmeans_folder if f"\\{dataset_name}" in x][0]
        kmeans_data = uf.import_pkl_file(kmeans_loc)

        # Collect the article ids for each of the clusters
        # article_ids = {topic:{} for topic in marginal_data.keys()}
        # for t in marginal_data.keys():
        #     for cluster_id in marginal_data[t]:
        #         cluster_elts = [x['article_id'] for x in kmeans_data[t]['narratives_classified'] if x['cluster_index']==cluster_id]
        #         article_ids[t][cluster_id] = cluster_elts
        article_ids = collect_article_ids(marginal_data, kmeans_data)

        # Get corresponding unstructured text
        # text_loc = uf.load_files_from_prepped_datasets([dataset_name])[0]
        # text_data = uf.import_csv(text_loc)
        # newspapers = {topic:{} for topic in article_ids.keys()}
        # for t in article_ids.keys():
        #     for c in article_ids[t]:
        #         newspapers[t][c] = []
        #         for a_id in article_ids[t][c]:
        #             newspaper = [x[8] for x in text_data if x[0]==a_id][0]
        #             newspapers[t][c].append(newspaper)
        newspapers = get_unstructured_text_elts(dataset_name,article_ids)
        marginal_newspapers[dataset_name] = newspapers
    uf.content_json_export(f'{title}_marginal_newspapers.json',marginal_newspapers)


def find_top_first_mainstreamed_newspapers(fs_mainstream_files, kmeans_files, title):
    mainstream_newspapers = {}
    for ds in fs_mainstream_files:

        # Get corresponding kmeans data
        kmeans_loc = [x for x in kmeans_files if f"\\{ds}" in x ][0]
        kmeans_data = uf.import_pkl_file(kmeans_loc)

        # Collect article ids
        article_ids = collect_article_ids(fs_mainstream_files[ds], kmeans_data)

        # Get corresponding unstructured text
        newspapers = get_unstructured_text_elts(ds, article_ids)
        mainstream_newspapers[ds] = newspapers

    uf.content_json_export(export_name=f"{title}_fs_mainstreamed_newspapers.json",data=mainstream_newspapers)

def find_top_sec_mainstreamed_newspapers(ss_mainstream_files, kmeans_files, title):
    mainstream_newspapers = {}
    for ds in ss_mainstream_files:
        # Get corresponding kmeans data
        kmeans_loc = [x for x in kmeans_files if f"\\{ds}" in x][0]
        kmeans_data = uf.import_pkl_file(kmeans_loc)

        # Collect article ids
        article_ids = collect_article_ids(ss_mainstream_files[ds], kmeans_data)

        # Get corresponding unstructured text
        newspapers = get_unstructured_text_elts(ds, article_ids)
        mainstream_newspapers[ds] = newspapers
    uf.content_json_export(export_name=f"{title}_ss_mainstreamed_newspapers.json", data=mainstream_newspapers)

def analyze_common_newspapers(title, level:str):
    if level=='marginal':
        filename = f'{title}_marginal_newspapers'
    if level=='fs_mainstreamed':
        filename = f'{title}_fs_mainstreamed_newspapers'
    if level=="ss_mainstreamed":
        filename = f"{title}_ss_mainstreamed_newspapers"
    newspaper_data = uf.import_json_content(f"{filename}.json")
    exportable = []
    for ds in newspaper_data.keys():
        for t in newspaper_data[ds].keys():
            all_newspapers = []
            for c_id in newspaper_data[ds][t].keys():
                all_newspapers += newspaper_data[ds][t][c_id]
            if all_newspapers == []:
                continue
            counter = Counter(all_newspapers)
            top_three = counter.most_common(3)
            row = [ds, t]
            for tup in top_three:
                row.append(tup[0])
                row.append(tup[1])

            exportable.append(row)
    uf.export_nested_list(f"{filename}.csv",exportable)


find_top_marginal_newspapers(marg_nosent_97_2_loc, kmeans_97_20, "Nosent_97_2")
find_top_marginal_newspapers(marg_nosent_97_3_loc, kmeans_97_30, "Nosent_97_3")
find_top_marginal_newspapers(marg_nosent_98_2_loc, kmeans_98_20, "Nosent_98_2")
find_top_marginal_newspapers(marg_nosent_98_3_loc, kmeans_98_20, "Nosent_98_3")

analyze_common_newspapers("Nosent_97_2", 'marginal')
analyze_common_newspapers("Nosent_97_3", 'marginal')
analyze_common_newspapers("Nosent_98_2", 'marginal')
analyze_common_newspapers("Nosent_98_3", 'marginal')
#
find_top_first_mainstreamed_newspapers(fs_mainstream_files=fs_nosent_97_20_main,
                                       kmeans_files=kmeans_97_20, title="Nosent_97_2")
find_top_first_mainstreamed_newspapers(fs_mainstream_files=fs_nosent_97_30_main,
                                       kmeans_files=kmeans_97_30, title="Nosent_97_3")
find_top_first_mainstreamed_newspapers(fs_mainstream_files=fs_nosent_98_20_main,
                                       kmeans_files=kmeans_98_20, title="Nosent_98_2")
find_top_first_mainstreamed_newspapers(fs_mainstream_files=fs_nosent_98_30_main,
                                       kmeans_files=kmeans_98_30, title="Nosent_98_3")

analyze_common_newspapers("Nosent_97_2", 'fs_mainstreamed')
analyze_common_newspapers("Nosent_97_3", 'fs_mainstreamed')
analyze_common_newspapers("Nosent_98_2", 'fs_mainstreamed')
analyze_common_newspapers("Nosent_98_3", 'fs_mainstreamed')

find_top_sec_mainstreamed_newspapers(ss_mainstream_files=ss_nosent_97_20_main, kmeans_files=kmeans_97_20,
                                     title="Nosent_97_2")
find_top_sec_mainstreamed_newspapers(ss_mainstream_files=ss_nosent_97_30_main, kmeans_files=kmeans_97_30,
                                     title="Nosent_97_3")
find_top_sec_mainstreamed_newspapers(ss_mainstream_files=ss_nosent_98_20_main, kmeans_files=kmeans_98_20,
                                     title="Nosent_98_2")
find_top_sec_mainstreamed_newspapers(ss_mainstream_files=ss_nosent_98_30_main, kmeans_files=kmeans_98_30,
                                     title="Nosent_98_3")

analyze_common_newspapers("Nosent_97_2", 'ss_mainstreamed')
analyze_common_newspapers("Nosent_97_3", 'ss_mainstreamed')
analyze_common_newspapers("Nosent_98_2", 'ss_mainstreamed')
analyze_common_newspapers("Nosent_98_3", 'ss_mainstreamed')