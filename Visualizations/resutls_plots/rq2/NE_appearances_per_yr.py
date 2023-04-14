# Scatter plot: x axis , y axis # of NE appearances
import matplotlib.pyplot as plt
import universal_functions as uf
from Results.locations import *

# x axis year
# y axis NE appearances
# one line per topic


def get_num_NEs(part, classification, cluster_type, topic):
    direct_files = [x for x in uf.get_files_from_folder(f"{uf.thesis_location}Results\\rq_2\\no_sent\\cosine_{classification}\\",
                                                        "json") if "direct_NEs" in x and cluster_type in x]
    periph_files = [x for x in uf.get_files_from_folder(f"{uf.thesis_location}Results\\rq_2\\no_sent\\cosine_{classification}\\",
                                                        "json") if "periph_NEs" in x and cluster_type in x]
    num_nes=0
    for file in direct_files + periph_files:
        data = uf.import_json_content(file)

        for k in data.keys():
            try:
                for marg_cluster_id in data[k][topic].keys():
                    for fs_ds in data[k][topic][marg_cluster_id].keys():
                        for fs_cluster_id in data[k][topic][marg_cluster_id][fs_ds].keys():
                            if 'direct' in file:
                                if str(part) in fs_ds:
                                    num_nes += len(data[k][topic][marg_cluster_id][fs_ds][fs_cluster_id])
                                continue
                            for ss_ds in data[k][topic][marg_cluster_id][fs_ds][fs_cluster_id].keys():
                                for ss_cluster_id in data[k][topic][marg_cluster_id][fs_ds][fs_cluster_id][ss_ds]:
                                    if str(part) in ss_ds:
                                        num_nes += len(ss_cluster_id)
            except KeyError:
                continue
    return num_nes


def plot_NEs_by_partisanship_topic(classification, cluster_type):
    # ASSUMING looking only at directly and peripherally mainstreamed narrative instances
    pipeline_conversion = {"97":{"0.2":"Low Clustering, Low Classification",
                                 "0.3":"High Clustering, Low Classification"},
                           "98":{"0.2":"Low Clustering, High Classification",
                                 "0.3":"High Clustering, High Classification"}}

    partisanships = ["FarRight","Right","CenterRight","Center","CenterLeft","Left","FarLeft"]

    for topic in ["Immigration","Islamophobia","Anti-semitism","Transphobia"]:
        y = []
        for part in partisanships :
            y.append(get_num_NEs(part, classification, cluster_type, topic))

        plt.plot(partisanships, y, label=f"{topic}")
    plt.legend()
    plt.xlabel("Partisanship")
    plt.ylabel("Number of Named Entities per Narrative")
    plt.title(f"{pipeline_conversion[classification][cluster_type]}: Number of Named Entities per Narrative by Partisanship")
    plt.show()


def plot_NEs_by_year_topic(classification, cluster_type):
    # ASSUMING looking only at directly and peripherally mainstreamed narrative instances
    pipeline_conversion = {"97":{"0.2":"Low Clustering, Low Classification",
                                 "0.3":"High Clustering, Low Classification"},
                           "98":{"0.2":"Low Clustering, High Classification",
                                 "0.3":"High Clustering, High Classification"}}

    years = [2016,2017,2018,2019,2020]
    for topic in ["Immigration","Islamophobia","Anti-semitism","Transphobia"]:
        y = []
        for yr in years:
            y.append(get_num_NEs(yr, classification, cluster_type, topic))

        plt.plot(years, y, label=f"{topic}")
    plt.legend()
    plt.xlabel("Year")
    plt.ylabel("Number of Named Entities per Narrative")
    plt.title(f"{pipeline_conversion[classification][cluster_type]}: Number of Named Entities per Narrative by Partisanship")
    plt.show()

for classification in ["97","98"]:
    for cluster_type in ["0.2","0.3"]:
        plot_NEs_by_partisanship_topic(classification, cluster_type)


# for classification in ["97","98"]:
#     for cluster_type in ["0.2","0.3"]:
#         plot_NEs_by_year_topic(classification, cluster_type)