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
                if newspaper not in newspapers[t][c]:
                    newspapers[t][c].append(newspaper)
    return newspapers


def find_pusher_candidates(marginal_files:list, kmeans_folder:list, title:str):
    marginal_newspapers = {}
    for loc in marginal_files:
        # Get marginal narratives
        marginal_data = uf.import_json_content(loc)
        dataset_name = uf.get_dataset_id(loc)

        # Get corresponding kmeans clustering
        kmeans_loc = [x for x in kmeans_folder if f"\\{dataset_name}" in x][0]
        kmeans_data = uf.import_pkl_file(kmeans_loc)

        # Collect the article ids for each of the clusters
        article_ids = collect_article_ids(marginal_data, kmeans_data)

        # Get corresponding unstructured text
        newspapers = get_unstructured_text_elts(dataset_name,article_ids)
        marginal_newspapers[dataset_name] = newspapers
    uf.content_json_export(f'{title}_pusher_candidates.json',marginal_newspapers)


def find_find_successful_pushers(mainstreamed_files, kmeans_files, title):
    mainstream_newspapers = {}
    for file in mainstreamed_files:
        data = uf.import_json_content(file)
        ds = list(data.keys())[0]

        # Get corresponding kmeans data
        kmeans_loc = [x for x in kmeans_files if f"\\{ds}" in x ][0]
        kmeans_data = uf.import_pkl_file(kmeans_loc)

        # Collect article ids
        article_ids = collect_article_ids(data[ds], kmeans_data)

        # Get corresponding unstructured text
        newspapers = get_unstructured_text_elts(ds, article_ids)
        mainstream_newspapers[ds] = newspapers

    uf.content_json_export(export_name=f"{title}_fs_pushers.json",data=mainstream_newspapers)

def find_sec_step_successful_pushers(ss_mainstream_files, kmeans_files, title):
    mainstream_newspapers = {}
    for file in ss_mainstream_files:
        # Get corresponding kmeans data
        kmeans_loc = [x for x in kmeans_files if f"\\{ds}" in x][0]
        kmeans_data = uf.import_pkl_file(kmeans_loc)

        # Collect article ids
        article_ids = collect_article_ids(ss_mainstream_files[ds], kmeans_data)

        # Get corresponding unstructured text
        newspapers = get_unstructured_text_elts(ds, article_ids)
        mainstream_newspapers[ds] = newspapers
    uf.content_json_export(export_name=f"{title}_ss_pushers.json", data=mainstream_newspapers)

def analyze_common_newspapers(title, level:str):
    if level=='pusher_candidates':
        filename = f'{title}_pusher_candidates'
    if level=='fs':
        filename = f'{title}_fs_pushers'
    if level=="ss":
        filename = f"{title}_ss_pushers"
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
            # top_three = counter.most_common(3)

            for n in counter.keys():
                row = [ds, t]
                row.append(n)
                row.append(counter[n])
                exportable.append(row)
    uf.export_nested_list(f"{filename}.csv",exportable)


def never_candidate(marginal_newspapers, title):
    pusher_cands = {}
    for x in marginal_newspapers:
        if x[0] not in pusher_cands.keys():
            pusher_cands[x[0]] = []
        pusher_cands[x[0]].append(x[-2])

    never_cands = {k: [] for k in pusher_cands.keys()}
    for ds in pusher_cands.keys():
        text_loc = uf.load_files_from_prepped_datasets([ds])[0]
        text_data = uf.import_csv(text_loc)
        for row in text_data:
            if row[8] not in pusher_cands[ds]:
                never_cands[ds].append(row[8])

    exportable = []
    for k in never_cands.keys():
        counter = Counter(never_cands[k])
        for c in counter.keys():
            row = [k]
            row.append(c)
            row.append(counter[c])
            exportable.append(row)
    uf.export_nested_list(f"{title}_never_pusher_cands.csv", exportable)

# find_pusher_candidates(marg_nosent_97_2_loc, kmeans_97_20, "no_sent/cosine_97/20")
# find_pusher_candidates(marg_nosent_97_3_loc, kmeans_97_30, "no_sent/cosine_97/30")
# find_pusher_candidates(marg_nosent_98_2_loc, kmeans_98_20, "no_sent/cosine_98/20")
# find_pusher_candidates(marg_nosent_98_3_loc, kmeans_98_20, "no_sent/cosine_98/30")
#
# analyze_common_newspapers("no_sent/cosine_97/20", 'pusher_candidates')
# analyze_common_newspapers("no_sent/cosine_97/30", 'pusher_candidates')
# analyze_common_newspapers("no_sent/cosine_98/20", 'pusher_candidates')
# analyze_common_newspapers("no_sent/cosine_98/30", 'pusher_candidates')

find_find_successful_pushers(mainstreamed_files=dir_narr_97_20,
                            kmeans_files=kmeans_97_20, title="no_sent/cosine_97/20")
find_find_successful_pushers(mainstreamed_files=dir_narr_97_30,
                            kmeans_files=kmeans_97_30, title="no_sent/cosine_97/30")
find_find_successful_pushers(mainstreamed_files=dir_narr_98_20,
                            kmeans_files=kmeans_98_20, title="no_sent/cosine_98/20")
find_find_successful_pushers(mainstreamed_files=dir_narr_98_30,
                            kmeans_files=kmeans_98_30, title="no_sent/cosine_98/30")

analyze_common_newspapers("no_sent/cosine_97/20", 'fs')
analyze_common_newspapers("no_sent/cosine_97/30", 'fs')
analyze_common_newspapers("no_sent/cosine_98/20", 'fs')
analyze_common_newspapers("no_sent/cosine_98/30", 'fs')

# find_sec_step_successful_pushers(ss_mainstream_files=ss_nosent_97_20_main, kmeans_files=kmeans_97_20,
#                                  title="no_sent/cosine_97/20")
# find_sec_step_successful_pushers(ss_mainstream_files=ss_nosent_97_30_main, kmeans_files=kmeans_97_30,
#                                  title="no_sent/cosine_97/30")
# find_sec_step_successful_pushers(ss_mainstream_files=ss_nosent_98_20_main, kmeans_files=kmeans_98_20,
#                                  title="no_sent/cosine_98/20")
# find_sec_step_successful_pushers(ss_mainstream_files=ss_nosent_98_30_main, kmeans_files=kmeans_98_30,
#                                  title="no_sent/cosine_98/30")
#
# analyze_common_newspapers("no_sent/cosine_97/20", 'ss')
# analyze_common_newspapers("no_sent/cosine_97/30", 'ss')
# analyze_common_newspapers("no_sent/cosine_98/20", 'ss')
# analyze_common_newspapers("no_sent/cosine_98/30", 'ss')

cosine_97_folder = uf.get_files_from_folder(f"no_sent/cosine_97/","csv")
cosine_98_folder = uf.get_files_from_folder(f"no_sent/cosine_98/","csv")

for file in cosine_97_folder:
    if 'pusher_candidates' not in file:
        continue
    if '20' in file:
        cluster = '20'
    if '30' in file:
        cluster = '30'
    pusher_cands = uf.import_csv(file)

    never_candidate(pusher_cands, title=f'no_sent/cosine_97/{cluster}')

for file in cosine_98_folder:
    if 'pusher_candidates' not in file:
        continue
    if '20' in file:
        cluster = '20'
    if '30' in file:
        cluster = '30'
    pusher_cands = uf.import_csv(file)

    never_candidate(pusher_cands, title=f'no_sent/cosine_98/{cluster}')

