from Results.locations import *
import matplotlib.pyplot as plt

def num_narratives_by_year_per_topic(topic):
    labels = ['Low Clusters, Low Classification',
              'High Clusters, Low Classification',
              'Low Clusters, High Classification',
              'High Clusters, High Classification']
    years = ['2016','2017','2018','2019','2020']

    pipelines = [kmeans_97_20, kmeans_97_30, kmeans_98_20, kmeans_98_30]

    for j in range(len(pipelines)):

        x = ['2016','2017','2018','2019','2020']
        y = [0,0,0,0,0]
        for file in pipelines[j]:
            if 'emoji' in file:
                continue
            try:
                year_index = [i for i in range(len(years)) if years[i] in file][0]
            except IndexError:
                continue
            data = uf.import_pkl_file(file)

            try:
                y[year_index] += data[topic]['num_clusters']
            except KeyError:
                continue
        plt.plot(x,y, label=labels[j])
    plt.title(f"{topic} Narrative Instances by Year")
    plt.xlabel('Year')
    plt.ylabel('Number of Narrative Instances')
    plt.legend()
    plt.show()


def plot_num_fr_narratives_by_yr_per_topic(topic):
    labels = ['Low Clusters, Low Classification',
              'High Clusters, Low Classification',
              'Low Clusters, High Classification',
              'High Clusters, High Classification']
    years = ['2016', '2017', '2018', '2019', '2020']

    pipelines = [kmeans_97_20, kmeans_97_30, kmeans_98_20, kmeans_98_30]

    for j in range(len(pipelines)):
        x = ['2016', '2017', '2018', '2019', '2020']
        y = [0, 0, 0, 0, 0]
        for file in pipelines[j]:
            if 'emoji' in file:
                continue
            if "FarRight" not in file:
                continue

            try:
                year_index = [i for i in range(len(years)) if years[i] in file][0]
            except IndexError:
                continue
            data = uf.import_pkl_file(file)

            try:
                y[year_index] += data[topic]['num_clusters']
            except KeyError:
                continue
        plt.plot(x, y, label=labels[j])
    plt.title(f"Far Right {topic} Narrative Instances by Year")
    plt.xlabel('Year')
    plt.ylabel('Number of Narrative Instances')
    plt.legend()
    plt.show()

plot_num_fr_narratives_by_yr_per_topic("Transphobia")
num_narratives_by_year_per_topic("Transphobia")
