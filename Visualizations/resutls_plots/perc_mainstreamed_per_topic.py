"Complete"
from Results.locations import *
import matplotlib.pyplot as plt
import numpy as np

# x axis: pipeline modification
# y axis:  # mainstreamed / # marginal narratives

def get_data(all_narr_folder):
    topics = ['Immigration','Islamophobia','Anti-semitism','Transphobia']
    results = {}
    for file in all_narr_folder:
        data = uf.import_json_content(file)

        direct_loc = file.replace('all_marginal_narr_matches','direct_mainstreamed_narratives')
        direct_data = uf.import_json_content(direct_loc)

        for ds in data.keys():
            year = ds[-4:]
            if year not in results.keys():
                results[year] = {}

            for t in topics:
                if t not in results[year].keys():
                    results[year][t] = {'marg_narratives': 0, 'num_mainstreamed_narratives': 0}
                try:
                    num_marg_narratives = len(data[ds][t])
                except KeyError:
                    num_marg_narratives = 0
                results[year][t]['marg_narratives'] += num_marg_narratives

        for t in topics:
            try:
                num_main_narratives = len(direct_data[ds][t])
            except KeyError:
                num_main_narratives = 0
            results[year][t]['num_mainstreamed_narratives'] += num_main_narratives

    Y = []
    for yr in results.keys():
        y = []
        for t in results[yr].keys():
            try:
                y.append(results[yr][t]['num_mainstreamed_narratives']/results[yr][t]['marg_narratives'])
            except ZeroDivisionError:
                y.append(0)
        Y.append(y)
    # transpose
    x = list(results.keys())
    combined = []
    transposed = np.array(Y).transpose().tolist()
    for i in range(len(transposed)):
        combined.append([x, transposed[i]])
    return combined, topics

def plot_data(combined, labels, title):

    for i in range(len(combined)):
        row = combined[i]
        plt.plot(row[0], row[1],  label=labels[i])
    plt.legend()
    plt.xlabel('Year of Marginal Narrative Origin')
    plt.ylabel('Ratio of Directly Mainstreamed Narratives to All Marginal Narratives')
    plt.title( f'{title}: Proportion Narratives Mainstreamed over time ')
    plt.show()

titles = ['Low Clusters, Low Classification',
          'High Clusters, Low Classification',
          'Low Clusters, High Classification',
          'High Clusters, High Classification']

all_narrs = [all_narr_97_20, all_narr_97_30, all_narr_98_20, all_narr_98_30]
for i in range(len(all_narrs)):
    narr = all_narrs[i]
    combined, labels = get_data(narr)
    plot_data(combined, labels, titles[i])