"""
COMPLETE
"""
import universal_functions as uf
import matplotlib.pyplot as plt
from Results.locations import *
# x axis = year
# y axis = # marg narratives per pipeline

def get_data(all_narr_folder):
    results = {}
    for file in all_narr_folder:
        data = uf.import_json_content(file)

        for ds in data.keys():
            year = ds[-4:]
            if year not in results.keys():
                results[year] = 0

            for t in data[ds].keys():
                num_marg_narratives = len(data[ds][t])
                results[year] += num_marg_narratives


    x, y = [],[]
    for yr in results.keys():
        x.append(yr)
        y.append(results[yr])
    return [x,y]

def get_topic_data(all_narr_folder, topic):
    results = {}
    for file in all_narr_folder:
        data = uf.import_json_content(file)

        for ds in data.keys():
            year = ds[-4:]
            if year not in results.keys():
                results[year] = 0

            try:
                num_marg_narratives = len(data[ds][topic])
            except KeyError:
                continue
            results[year] += num_marg_narratives


    x, y = [],[]
    for yr in results.keys():
        x.append(yr)
        y.append(results[yr])
    return [x,y]


def num_marg_narr_by_year_pipeline():
    x_y_97_20 = get_data(all_narr_97_20)
    x_y_97_30 = get_data(all_narr_97_30)
    x_y_98_20 = get_data(all_narr_98_20)
    x_y_98_30 = get_data(all_narr_98_30)
    combined = [x_y_97_20,x_y_97_30,x_y_98_20,x_y_98_30]
    labels = ['Low Clusters, Low Classification',
              'High Clusters, Low Classification',
              'Low Clusters, High Classification',
              'High Clusters, High Classification']


    for i in range(len(combined)):
        row = combined[i]
        plt.plot(row[0], row[1],  label=labels[i])
    plt.legend()
    plt.xlabel('Year of Marginal Narrative Origin')
    plt.ylabel('Number of Marginal Narratives')
    plt.title('Number of Marginal Narratives over time ')
    plt.show()

def num_marg_narr_by_topic_pipeline(topic):
    x_y_97_20 = get_topic_data(all_narr_97_20,topic)
    x_y_97_30 = get_topic_data(all_narr_97_30,topic)
    x_y_98_20 = get_topic_data(all_narr_98_20,topic)
    x_y_98_30 = get_topic_data(all_narr_98_30,topic)
    combined = [x_y_97_20, x_y_97_30, x_y_98_20, x_y_98_30]
    labels = ['Low Clusters, Low Classification',
              'High Clusters, Low Classification',
              'Low Clusters, High Classification',
              'High Clusters, High Classification']

    for i in range(len(combined)):
        row = combined[i]
        plt.plot(row[0], row[1], label=labels[i])
    plt.legend()
    plt.xlabel('Year of Marginal Narrative Origin')
    plt.ylabel('Number of Marginal Narratives')
    plt.title(f'Number of {topic} Marginal Narratives over time ')
    plt.show()

num_marg_narr_by_topic_pipeline("Transphobia")