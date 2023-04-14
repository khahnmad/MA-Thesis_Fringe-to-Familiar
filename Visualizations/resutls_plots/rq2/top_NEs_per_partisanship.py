import universal_functions as uf
from collections import Counter
from typing import List
import matplotlib.pyplot as plt

from nltk.corpus import stopwords
stop = stopwords.words('english')

def query_appearances(word, topic, loc, cluster_type, partisanship):
    # finds the absolute number of appearances, not number of narratives in which it appears
    # files = [f"{loc}FarRight_2-2016_{cluster_type}_direct_NEs.json",f"{loc}_periph_NEs.json"]
    files = [x for x in uf.get_files_from_folder(loc,'json') if cluster_type in x and 'direct_NEs' in x ] +\
            [x for x in uf.get_files_from_folder(loc,'json') if cluster_type in x and 'periph_NE' in x ]
    appearances = []
    for file in files:
        try:
            data = uf.import_json_content(file)
        except FileNotFoundError:
            continue
        for k in data.keys():
            try:
                for marg_cluster_id in data[k][topic].keys():
                    for fs_ds in data[k][topic][marg_cluster_id].keys():
                        for fs_cluster_id in data[k][topic][marg_cluster_id][fs_ds].keys():
                            if 'direct' in file:
                                if partisanship in fs_ds:
                                    appearances +=[x[0] for x in data[k][topic][marg_cluster_id][fs_ds][fs_cluster_id] if x[0]==word]
                                continue
                            for ss_ds in data[k][topic][marg_cluster_id][fs_ds][fs_cluster_id].keys():
                                for ss_cluster in data[k][topic][marg_cluster_id][fs_ds][fs_cluster_id][ss_ds]:
                                    if partisanship in ss_ds:
                                        appearances +=[x[0] for x in ss_cluster if x[0]==word]
            except KeyError:
                continue
    return len(appearances)


def get_top_NEs(topic:str, loc:str, cluster_type:str)->List[str]:
    # ASSUMING mainstream
    # ASSUMING top 6
    direct_files = [x for x in uf.get_files_from_folder(loc,'json') if 'direct_NEs' in x and cluster_type in x]
    all_nes = []
    for file in direct_files:
        data = uf.import_json_content(file)
        for k in data.keys():
            try:
                for marg_cluster_id in data[k][topic].keys():
                    for fs_ds in data[k][topic][marg_cluster_id].keys():
                        for fs_cluster_id in data[k][topic][marg_cluster_id][fs_ds].keys():
                            all_nes += uf.remove_duplicates([x[0] for x in data[k][topic][marg_cluster_id][fs_ds][fs_cluster_id]])
            except KeyError:
                continue
    periph_files = [x for x in uf.get_files_from_folder(loc,'json') if 'periph_NEs' in x and cluster_type in x]
    for file in periph_files:
        data = uf.import_json_content(file)
        for k in data.keys():
            try:
                for marg_cluster_id in data[k][topic].keys():
                    for fs_ds in data[k][topic][marg_cluster_id].keys():
                        for fs_cluster_id in data[k][topic][marg_cluster_id][fs_ds].keys():
                            for ss_ds in data[k][topic][marg_cluster_id][fs_ds][fs_cluster_id].keys():
                                for ss_cluster in data[k][topic][marg_cluster_id][fs_ds][fs_cluster_id][ss_ds]:
                                    all_nes += uf.remove_duplicates([x[0] for x in ss_cluster])
            except KeyError:
                continue
    clened_nes = [x for x in all_nes if x.lower() not in stop]
    counter = Counter(clened_nes).most_common(6)
    top = []
    for tup in counter:
        top.append(tup[0])
    return top


def plot_top_NEs_by_topic_per_pipeline(loc, cluster_type):
    title_conversion =  {"97\\":{"0.2": "Low Clusters, Low Classification",
                                 "0.3": "High Clusters, Low Classification"},
                         "98\\":{"0.2": "Low Clusters, High Classification",
                                 "0.3": "High Clusters, High Classification"}}
    part = ["FarRight",'Right',"CenterRight",'Center',"CenterLeft","Left","FarLeft"]
    for topic in ['Immigration', 'Islamophobia','Anti-semitism','Transphobia']:
        top_marg = get_top_NEs(topic, loc, cluster_type)
        results = {}
        for word in top_marg:
            results[word] = []
            for p in part:
                results[word].append(query_appearances(word, topic, loc, cluster_type, p))

        for w in results.keys():
            plt.plot(part, results[w], label=f"{w}")
        plt.title(f"{title_conversion[loc[-3:]][cluster_type]}, {topic}: Number of Appearances of Top Entities by Partisanship")
        plt.xlabel('Year')
        plt.ylabel('Number of Appearances')
        plt.legend()
        plt.show()

def plot_top_NEs_per_partisansip():
    for loc in [f"{uf.thesis_location}Results\\rq_2\\no_sent\\cosine_97\\",
                f"{uf.thesis_location}Results\\rq_2\\no_sent\\cosine_98\\"]:
        for cluster_type in ["0.2","0.3"]:
            plot_top_NEs_by_topic_per_pipeline(loc, cluster_type)


plot_top_NEs_per_partisansip()