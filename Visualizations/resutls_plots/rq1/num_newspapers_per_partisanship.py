"""COMPLETE"""
# x axis : partisanship
# y axis: number of newspapers
# line for each topic in the pipeline modification

import universal_functions as uf
from Results.locations import *
import matplotlib.pyplot as plt

def get_num_newspapers(partisanship, classification, cluster_type, topic):
    loc = f"{uf.thesis_location}Results\\pullers\\no_sent\\cosine_{classification}\\{cluster_type}_pullers.csv"
    data = uf.import_csv(loc)
    newspapers = [x for x in data if x[1]==topic and x[2]==partisanship]
    return len(newspapers)


def plot_newspapers_by_partisanship_and_topic(classification, cluster_type):
    # ASSUMING looking only at directly and peripherally mainstreamed narrative instances
    pipeline_conversion = {"97":{"20":"Low Clustering, Low Classification",
                                 "30":"High Clustering, Low Classification"},
                           "98":{"20":"Low Clustering, High Classification",
                                 "30":"High Clustering, High Classification"}}
    partisanships = ["FarRight","Right","CenterRight","Center","CenterLeft","Left","FarLeft"]
    for topic in ["Immigration","Islamophobia","Anti-semitism","Transphobia"]:
        y = []
        for part in partisanships :
            y.append(get_num_newspapers(part, classification, cluster_type, topic))

        plt.plot(partisanships, y, label=f"{topic}")
    plt.legend()
    plt.xlabel("Partisanship")
    plt.ylabel("Number of Newspapers per Narrative Instance")
    plt.title(f"{pipeline_conversion[classification][cluster_type]}: Number of Newspapers Contributing to Mainstreamed Narrative Instances")
    plt.show()


for classification in ["97","98"]:
    for cluster_type in ["20","30"]:
        plot_newspapers_by_partisanship_and_topic(classification, cluster_type)