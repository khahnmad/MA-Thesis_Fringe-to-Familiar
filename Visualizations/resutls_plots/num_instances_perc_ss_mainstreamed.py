from Results.locations import *
from collections import Counter
import matplotlib.pyplot as plt

# x axis: number of fs mainstreamed narrative instances
# y axis: number of ss mainstreamed narrative instances

def get_num_periph_instances_perc_ss_mainstreamd(all_narr_folder):
    ss_matches = {}
    x,y = [],[]
    for file in all_narr_folder:
        data = uf.import_json_content(file)
        ds_name = list(data.keys())[0]
        data = data[ds_name]


        for t in data.keys():
            for marg_cluster_id in data[t].keys():
                ss_matches[f"{ds_name}_{t}_{marg_cluster_id}"] = []

                for fs_ds in data[t][marg_cluster_id].keys():
                    for fs_cluster_id in data[t][marg_cluster_id][fs_ds].keys():
                        for ss_ds in data[t][marg_cluster_id][fs_ds][fs_cluster_id].keys():
                            ss_cluster_ids = data[t][marg_cluster_id][fs_ds][fs_cluster_id][ss_ds]
                            ss_matches[f"{ds_name}_{t}_{marg_cluster_id}"]+=[ss_ds for x in ss_cluster_ids]



    for t_marg_id in ss_matches.keys():
        num_instances = len(ss_matches[t_marg_id])
        if num_instances == 0:
            perc_mainstreamed = 0
        else:
            counter = Counter([x[:-7] for x in ss_matches[t_marg_id]])
            centers = 0
            for c in counter.keys():
                if "Center" in c:
                    centers+=counter[c]
            perc_mainstreamed = centers/ num_instances

        x.append(num_instances)
        y.append(perc_mainstreamed)
    return x,y

def scatter_plot(x,y, xlabel, ylabel, title):
    plt.scatter(x,y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.title(title)
    plt.show()

cosine_97_20_all_narr = [x for x in uf.get_files_from_folder(f"{uf.thesis_location}Tracking\\LowClass_Threshold","json") if '0.2' in x and 'emojj' not in x]
cosine_97_30_all_narr = [x for x in uf.get_files_from_folder(f"{uf.thesis_location}Tracking\\LowClass_Threshold","json") if '0.3' in x and 'emojj' not in x]

cosine_98_20_all_narr = [x for x in uf.get_files_from_folder(f"{uf.thesis_location}Tracking\\HighClass_Threshold","json") if '0.2' in x and 'emojj' not in x]
cosine_98_30_all_narr = [x for x in uf.get_files_from_folder(f"{uf.thesis_location}Tracking\\HighClass_Threshold","json") if '0.3' in x and 'emojj' not in x]



x,y =get_num_periph_instances_perc_ss_mainstreamd(cosine_97_20_all_narr)
scatter_plot(title="Few Clusters, Low Classification Threshold: Peripheral Narrative Instances by % Instances in the Center for all Marginal Narratives",
             xlabel='Number of Peripheral Match Instances',
             ylabel='% Narrative Instances in the Centrist Partisanships',
             x=x,
             y=y)

x,y =get_num_periph_instances_perc_ss_mainstreamd(cosine_97_30_all_narr)
scatter_plot(title="More Clusters, Low Classification Threshold: Narrative Instances by % Instances in the Center for all Marginal Narratives",
             xlabel='Number of Direct Match Instances',
             ylabel='% Narrative Instances in the Centrist Partisanships',
             x=x,
             y=y)

x,y =get_num_periph_instances_perc_ss_mainstreamd(cosine_98_20_all_narr)
scatter_plot(title="Few Clusters, High Classification Threshold: Narrative Instances by % Instances in the Center for all Marginal Narratives",
             xlabel='Number of Direct Match Instances',
             ylabel='% Narrative Instances in the Centrist Partisanships',
             x=x,
             y=y)

x,y =get_num_periph_instances_perc_ss_mainstreamd(cosine_98_30_all_narr)
scatter_plot(title="More Clusters, High Classification Threshold: Narrative Instances by % Instances in the Center for all Marginal Narratives",
             xlabel='Number of Direct Match Instances',
             ylabel='% Narrative Instances in the Centrist Partisanships',
             x=x,
             y=y)