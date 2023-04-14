import universal_functions as uf
import matplotlib.pyplot as plt
from collections import Counter
from typing import List

def get_top_NEs(topic:str, loc:str, cluster_type:str)->List[str]:
    # ASSUMING marginal
    # ASSUMING top 2
    marg_files = [x for x in uf.get_files_from_folder(loc,'json') if 'marginal_NEs' in x and cluster_type in x]
    all_nes = []
    for file in marg_files:
        data = uf.import_json_content(file)
        for k in data.keys():
            try:
                for marg_cluster_id in data[k][topic].keys():
                    all_nes += [x[0] for x in data[k][topic][marg_cluster_id]]
            except KeyError:
                continue
    counter = Counter(all_nes).most_common(2)
    top = []
    for tup in counter:
        top.append(tup[0])
    return top


def query_appearances(word, topic, file):
    # finds the absolute number of appearances, not number of narratives in which it appears
    data = uf.import_json_content(file)
    appearances = []
    for k in data.keys():
        try:
            for marg_cluster_id in data[k][topic].keys():
                if 'marginal' in file:
                    appearances+= [x[0] for x in data[k][topic][marg_cluster_id] if x[0]==word]
                    continue
                for fs_ds in data[k][topic][marg_cluster_id].keys():
                    for fs_cluster_id in data[k][topic][marg_cluster_id][fs_ds].keys():
                        if 'direct' in file:
                            appearances +=[x[0] for x in data[k][topic][marg_cluster_id][fs_ds][fs_cluster_id] if x[0]==word]
                            continue

                        for ss_ds in data[k][topic][marg_cluster_id][fs_ds][fs_cluster_id].keys():
                            for ss_cluster in data[k][topic][marg_cluster_id][fs_ds][fs_cluster_id][ss_ds]:
                                appearances +=[x[0] for x in ss_cluster if x[0]==word]
        except KeyError:
            continue
    return len(appearances)


def plot_top_NEs_over_time_per_pipeline(loc, cluster_type):
    years = [2016,2017,2018,2019,2020]
    for topic in ['Immigration', 'Islamophobia','Anti-semitism','Transphobia']:
        top_marg = get_top_NEs(topic, loc, cluster_type)
        results = {}
        for word in top_marg:
            results[word] = {'marg':[],"direct":[],'periph':[]}
            for year in years:
                results[word]['marg'].append(query_appearances(word, topic,
                                                               f"{loc}FarRight_2-{year}_{cluster_type}_marginal_NEs.json"))
                results[word]['direct'].append(query_appearances(word, topic,
                                                                 f"{loc}FarRight_2-{year}_{cluster_type}_direct_NEs.json"))
                results[word]['periph'].append(query_appearances(word, topic,
                                                                 f"{loc}FarRight_2-{year}_{cluster_type}_periph_NEs.json"))

        for w in results.keys():
            for type in results[w].keys():
                plt.plot(years, results[w][type], label=f"{type}: {w}")
        plt.title(f"{loc[-4:]}, {cluster_type}: {topic}")
        plt.legend()
        plt.show()

def plot_top_NEs_over_time():
    for loc in [f"{uf.thesis_location}Results\\rq_2\\no_sent\\cosine_97\\",
                f"{uf.thesis_location}Results\\rq_2\\no_sent\\cosine_98\\"]:
        for cluster_type in ["0.2","0.3"]:
            plot_top_NEs_over_time_per_pipeline(loc, cluster_type)

plot_top_NEs_over_time()