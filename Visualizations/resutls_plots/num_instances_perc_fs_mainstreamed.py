"""COMPLETE"""
from Results.locations import *
from collections import Counter
import matplotlib.pyplot as plt

# x axis: number of fs mainstreamed narrative instances
# y axis: number of ss mainstreamed narrative instances

def get_num_instances_perc_mainstreamd(fs_folder):
    x,y = [],[]
    for file in fs_folder:
        data = uf.import_json_content(file)
        ds_name = uf.get_dataset_id(file)

        for t in data.keys():
            for cluster_id in data[t].keys():
                num_instances = len(data[t][cluster_id])

                counter = Counter([x[0][:-7] for x in data[t][cluster_id]])
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

x,y =get_num_instances_perc_mainstreamd(fs_97_20_nosent)
scatter_plot(title="Few Clusters, Low Classification Threshold: Narrative Instances by % Instances in the Center for all Marginal Narratives",
             xlabel='Number of Direct Match Instances',
             ylabel='% Narrative Instances in the Centrist Partisanships',
             x=x,
             y=y)

x,y =get_num_instances_perc_mainstreamd(fs_97_30_nosent)
scatter_plot(title="More Clusters, Low Classification Threshold: Narrative Instances by % Instances in the Center for all Marginal Narratives",
             xlabel='Number of Direct Match Instances',
             ylabel='% Narrative Instances in the Centrist Partisanships',
             x=x,
             y=y)

x,y =get_num_instances_perc_mainstreamd(fs_98_20_nosent)
scatter_plot(title="Few Clusters, High Classification Threshold: Narrative Instances by % Instances in the Center for all Marginal Narratives",
             xlabel='Number of Direct Match Instances',
             ylabel='% Narrative Instances in the Centrist Partisanships',
             x=x,
             y=y)

x,y =get_num_instances_perc_mainstreamd(fs_98_30_nosent)
scatter_plot(title="More Clusters, High Classification Threshold: Narrative Instances by % Instances in the Center for all Marginal Narratives",
             xlabel='Number of Direct Match Instances',
             ylabel='% Narrative Instances in the Centrist Partisanships',
             x=x,
             y=y)