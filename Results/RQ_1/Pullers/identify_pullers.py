import universal_functions as uf

from Results.locations import *

from collections import Counter
import re

def convert_to_dict(nested_list):
    dict_form = {}
    for row in nested_list:
        if row[0] not in dict_form.keys():
            dict_form[row[0]] = {}
        if row[1] not in dict_form[row[0]].keys():
            dict_form[row[0]][row[1]] = {}
        if row[2] not in dict_form[row[0]][row[1]].keys():
            dict_form[row[0]][row[1]][row[2]] = []
        dict_form[row[0]][row[1]][row[2]].append([row[3],float(row[4])])
    return dict_form


def get_num_articles(newspaper, dataset, topic, title):

    news_art_ids = uf.import_json_content(f"../pushers/{title}_newspaper_appearances.json")
    result = 0
    for k in news_art_ids.keys():
        if dataset in k:
            try:
                result += news_art_ids[k][topic][newspaper]
            except KeyError:
                continue
    # result = news_art_ids[dataset][topic][newspaper]
    return result

def collect_article_ids(ds_name, topic, clusters, kmeans_files):
    kmeans_file = [x for x in kmeans_files if ds_name in x]
    kmeans_data = uf.import_pkl_file(kmeans_file[0])
    article_ids =[]
    for cluster_id in clusters:
        cluster_elts = [x['article_id'] for x in kmeans_data[topic]['narratives_classified'] if
                        x['cluster_index'] == int(cluster_id)]
        article_ids.append(cluster_elts)
    return article_ids


def get_dataset_partisanship(filename):
    regex = r"(.*?)(?=\_2-)"
    dataset_name = re.findall(regex, filename)[0]
    return dataset_name

def get_unstructured_text_elts(dataset_name, article_ids):
    if '0.2' in dataset_name or '0.3' in dataset_name:
        dataset_name = dataset_name[:-4]
    text_loc = uf.load_files_from_prepped_datasets([dataset_name])[0]
    text_data = uf.import_csv(text_loc)
    newspapers = []
    for cluster in article_ids:
        cluster_newspapers = []
        for a_id in cluster:
            newspaper = [x[8] for x in text_data if x[0] == a_id][0]
            if newspaper not in cluster_newspapers:
                cluster_newspapers.append(newspaper)
        newspapers+=cluster_newspapers
    return newspapers

def identify_puller_candidates(fs_files,kmeans_files, title):
    cand_clusters = {}
    for file in fs_files:
        data= uf.import_json_content(file)
        dataset_name = uf.get_dataset_id(file)

        cand_clusters[dataset_name] = {}
        for t in data.keys():
            cand_clusters[dataset_name][t] = {}
            for c in data[t].keys():
               for elt in data[t][c]:
                   if elt[0] not in cand_clusters[dataset_name][t].keys():
                       cand_clusters[dataset_name][t][elt[0]] = []
                   cand_clusters[dataset_name][t][elt[0]].append(elt[1])

    puller_cands ={}
    for ds in cand_clusters.keys():
        puller_cands[ds] ={}
        for t in cand_clusters[ds].keys():
            puller_cands[ds][t] = {}
            for match_ds in cand_clusters[ds][t].keys():
                p = get_dataset_partisanship(match_ds)
                if p not in puller_cands[ds][t].keys():
                    puller_cands[ds][t][p] = []
                art_ids = collect_article_ids(kmeans_files=kmeans_files, ds_name=match_ds, topic=t,
                                              clusters=cand_clusters[ds][t][match_ds])
                newspapers = get_unstructured_text_elts(match_ds, art_ids)
                puller_cands[ds][t][p]+=newspapers

    exportable = []
    for ds in puller_cands.keys():
        for t in puller_cands[ds].keys():
            for p in puller_cands[ds][t].keys():
                counter = Counter(puller_cands[ds][t][p])
                for c in counter.keys():
                    if counter[c]>1:
                        row = [ds, t, p, c, counter[c]]
                        exportable.append(row)
    uf.export_nested_list(f'{title}_puller_candidates.csv', exportable)

def identify_fs_pullers(kmeans_files, title, direct_files):
    print(f"Identifying first step pullers")
    cand_clusters ={}
    for file in direct_files: # Iterate through the directly mainstreamed files
        data= uf.import_json_content(file)
        ds_name = list(data.keys())[0]
        # dataset_name = uf.get_dataset_id(file)

        cand_clusters[ds_name] ={}

        # Get the fs cluster ids for the file
        for t in data[ds_name].keys(): # Iterate through the topics
            cand_clusters[ds_name][t] = {}

            for c in data[ds_name][t].keys(): # Iterate through the marginal cluster ids
                for fs_ds in data[ds_name][t][c].keys(): # iterate through the direct match datasets
                    if fs_ds not in cand_clusters[ds_name][t].keys():
                        cand_clusters[ds_name][t][fs_ds] = []
                    for fs_cluster_id in data[ds_name][t][c][fs_ds].keys():
                        cand_clusters[ds_name][t][fs_ds].append(fs_cluster_id)

    puller_cands = {}
    for ds in cand_clusters.keys(): # iterate through the starter year
        puller_cands[ds] = {}

        for t in cand_clusters[ds].keys(): # iterate through the topics
            puller_cands[ds][t] = {}
            for match_ds in cand_clusters[ds][t].keys(): # iterate through the fs ds
                p = get_dataset_partisanship(match_ds)

                if p not in puller_cands[ds][t].keys():
                    puller_cands[ds][t][p] = []
                art_ids = collect_article_ids(kmeans_files=kmeans_files, ds_name=match_ds, topic=t,
                                              clusters=cand_clusters[ds][t][match_ds])
                newspapers = get_unstructured_text_elts(match_ds, art_ids)
                puller_cands[ds][t][p] += newspapers

    exportable = []
    for ds in puller_cands.keys():
        for t in puller_cands[ds].keys():
            for p in puller_cands[ds][t].keys():
                counter = Counter(puller_cands[ds][t][p])
                for c in counter.keys():
                        row = [ds, t, p, c, counter[c]]
                        exportable.append(row)
    uf.export_nested_list(f'{title}_pullers.csv', exportable)

def top_puller_rel_num_articles(title):
    print(f"Running top puller relative to number of articles for {title}...")
    file = f"{title}_pullers.csv"
    puller_list = uf.import_csv(file)
    puller_dict = convert_to_dict(puller_list)

    exportable = []
    for ds in puller_dict.keys(): # Iterate through far ds
        for t in puller_dict[ds].keys(): # Iterate through topic
            for plat_part in puller_dict[ds][t].keys(): # Iterate through platforming partisanships
                for row in puller_dict[ds][t][plat_part]:
                    num_articles = get_num_articles(row[0], plat_part, t, title)
                    exportable.append([ds, t, plat_part, row[0], int(row[1]) / num_articles])
    uf.export_nested_list(f"{title}_fs_relative_to_newspapers.csv", exportable)

def find_absolute_top_relative(relative_dict):
    by_topic_center, by_topic_partisan = {}, {}
    by_year_center, by_year_partisan = {}, {}
    for ds in relative_dict.keys():  # Iterate through the FR datasets
        by_year_center[ds], by_year_partisan[ds] = {}, {}
        for t in relative_dict[ds].keys():  # Iterate through the topics
            if t not in by_topic_center.keys():
                by_topic_center[t], by_topic_partisan[t] = {}, {}
            for plt_part in relative_dict[ds][t].keys():  # Iterate through the paltforming partisanships
                if "Center" in plt_part:
                    for elt in relative_dict[ds][t][plt_part]:  # Iterate through the newspapers
                        if elt[0] not in by_topic_center[t].keys():
                            by_topic_center[t][elt[0]] = [elt[1]]
                        else:
                            by_topic_center[t][elt[0]] += [elt[1]]

                        if elt[0] not in by_year_center[ds].keys():
                            by_year_center[ds][elt[0]] = [elt[1]]
                        else:
                            by_year_center[ds][elt[0]] += [elt[1]]
                else:
                    for elt in relative_dict[ds][t][plt_part]:  # Iterate through the newspapers
                        n_title = f"{elt[0]}"
                        if n_title not in by_topic_partisan[t].keys():
                            by_topic_partisan[t][n_title] = [elt[1]]
                        else:
                            by_topic_partisan[t][n_title] += [elt[1]]

                        if n_title not in by_year_partisan[ds].keys():
                            by_year_partisan[ds][n_title] = [elt[1]]
                        else:
                            by_year_partisan[ds][n_title] += [elt[1]]
        for n in by_year_partisan[ds].keys():
            by_year_partisan[ds][n] = sum(by_year_partisan[ds][n])/len(by_year_partisan[ds][n])
        for n in by_year_center[ds].keys():
            by_year_center[ds][n] = sum(by_year_center[ds][n])/len(by_year_center[ds][n])
    for t in by_topic_partisan.keys():
        for n in by_topic_partisan[t].keys():
            by_topic_partisan[t][n] = sum(by_topic_partisan[t][n])/len(by_topic_partisan[t][n])
    for t in by_topic_center.keys():
        for n in by_topic_center[t].keys():
            by_topic_center[t][n] = sum(by_topic_center[t][n])/len(by_topic_center[t][n])

    by_year_center = get_max_values(by_year_center)
    by_year_partisan = get_max_values(by_year_partisan)
    by_topic_center = get_max_values(by_topic_center)
    by_topic_partisan = get_max_values(by_topic_partisan)
    return by_year_center, by_year_partisan, by_topic_center, by_topic_partisan


def get_max_values(dictionary):
    for k in dictionary.keys():
        if len(dictionary[k])>0:
            dictionary[k] = max(dictionary[k], key=dictionary[k].get)
    return dictionary

def find_absolute_top_pushers(top_pullers):
    by_topic_center, by_topic_partisan = {},{}
    by_year_center, by_year_partisan = {},{}
    for ds in top_pullers.keys(): # Iterate through the FR datasets
        by_year_center[ds], by_year_partisan[ds] ={},{}
        for t in top_pullers[ds].keys(): # Iterate through the topics
            if t not in by_topic_center.keys():
                by_topic_center[t], by_topic_partisan[t] = {},{}
            for plt_part in top_pullers[ds][t].keys(): # Iterate through the paltforming partisanships
                if "Center" in plt_part:
                    for elt in top_pullers[ds][t][plt_part]: # Iterate through the newspapers
                        if elt[0] not in by_topic_center[t].keys():
                            by_topic_center[t][elt[0]]=elt[1]
                        else:
                            by_topic_center[t][elt[0]] += elt[1]

                        if elt[0] not in by_year_center[ds].keys():
                            by_year_center[ds][elt[0]] = elt[1]
                        else:
                            by_year_center[ds][elt[0]] += elt[1]
                else:
                    for elt in top_pullers[ds][t][plt_part]: # Iterate through the newspapers
                        n_title = f"{elt[0]}"
                        if n_title not in by_topic_partisan[t].keys():
                            by_topic_partisan[t][n_title] = elt[1]
                        else:
                            by_topic_partisan[t][n_title] += elt[1]

                        if n_title not in by_year_partisan[ds].keys():
                            by_year_partisan[ds][n_title] = elt[1]
                        else:
                            by_year_partisan[ds][n_title] += elt[1]

    by_year_center = get_max_values(by_year_center)
    by_year_partisan = get_max_values(by_year_partisan)
    by_topic_center = get_max_values(by_topic_center)
    by_topic_partisan = get_max_values(by_topic_partisan)
    return by_year_center,by_year_partisan,by_topic_center,by_topic_partisan

def make_exportable(title, total, rel, part, axis):
    exportable = [[f'Top Puller By {axis}, {part}: {title}'],
                        [axis, "Absolute", "Relative"]]
    for k in total.keys():
        exportable.append([k, total[k], rel[k]])
    return exportable


def final_summary(title):
    print(f"Running final summary for {title}...")
    top_puller_data = uf.import_csv(f"{title}_pullers.csv")
    rel_to_news_data = uf.import_csv(f"{title}_fs_relative_to_newspapers.csv")

    top_pullers = convert_to_dict(top_puller_data)
    rel_to_news = convert_to_dict(rel_to_news_data)

    by_year_center,by_year_partisan,by_topic_center,by_topic_partisan = find_absolute_top_pushers(top_pullers)
    rel_by_year_center, rel_by_year_partisan,rel_by_topic_center, rel_by_topic_partisan  = find_absolute_top_relative(rel_to_news)

    uf.export_nested_list(f"{title}_top_puller_by_topic_center.csv",make_exportable(title, by_topic_center, rel_by_topic_center, 'Center', 'Topic'))
    uf.export_nested_list(f"{title}_top_puller_by_topic_partisan.csv",make_exportable(title, by_topic_partisan, rel_by_topic_partisan, 'Partisan', 'Topic'))

    uf.export_nested_list(f"{title}_top_puller_by_year_center.csv",
                          make_exportable(title, by_year_center, rel_by_year_center, 'Center', 'Year'))
    uf.export_nested_list(f"{title}_top_puller_by_year_partisan.csv",
                          make_exportable(title, by_year_partisan, rel_by_year_partisan, 'Partisan', 'Year'))
    print('check')

#
identify_puller_candidates(fs_97_20_nosent, kmeans_97_20, title="no_sent/cosine_97/20")
identify_puller_candidates(fs_97_30_nosent, kmeans_97_30, title="no_sent/cosine_97/30")
identify_puller_candidates(fs_98_20_nosent, kmeans_98_20, title="no_sent/cosine_98/20")
identify_puller_candidates(fs_98_30_nosent, kmeans_98_30, title="no_sent/cosine_98/30")

identify_fs_pullers(kmeans_files=kmeans_97_20, direct_files=dir_narr_97_20,
                    title='no_sent/cosine_97/20')
identify_fs_pullers(kmeans_files=kmeans_97_30, direct_files=dir_narr_97_30,
                    title='no_sent/cosine_97/30')
identify_fs_pullers(kmeans_files=kmeans_98_20, direct_files=dir_narr_98_20,
                    title='no_sent/cosine_98/20')
identify_fs_pullers(kmeans_files=kmeans_98_30, direct_files=dir_narr_98_30,
                    title='no_sent/cosine_98/30')

top_puller_rel_num_articles('no_sent/cosine_97/20')
top_puller_rel_num_articles('no_sent/cosine_97/30')
top_puller_rel_num_articles('no_sent/cosine_98/20')
top_puller_rel_num_articles('no_sent/cosine_98/30')

final_summary('no_sent/cosine_97/20')
final_summary('no_sent/cosine_97/30')
final_summary('no_sent/cosine_98/20')
final_summary('no_sent/cosine_98/30')


def identify_never_pullers():
    return