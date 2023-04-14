"""
COMPLETE
"""
from Results.locations import *
import matplotlib.pyplot as plt

# x axis: pipeline modification
# y axis:  # mainstreamed / # marginal narratives

def get_data(all_narr_folder):
    results = {}
    for file in all_narr_folder:
        data = uf.import_json_content(file)

        direct_loc = file.replace('all_marginal_narr_matches','direct_mainstreamed_narratives')
        direct_data = uf.import_json_content(direct_loc)

        for ds in data.keys():
            year = ds[-4:]
            if year not in results.keys():
                results[year] = {'marg_narratives':0, 'num_mainstreamed_narratives':0}

            for t in data[ds].keys():
                num_marg_narratives = len(data[ds][t])
                results[year]['marg_narratives'] += num_marg_narratives

        for t in direct_data[ds].keys():
            num_main_narratives = len(direct_data[ds][t])
            results[year]['num_mainstreamed_narratives'] += num_main_narratives
    x, y = [],[]
    for yr in results.keys():
        x.append(yr)
        y.append(results[yr]['num_mainstreamed_narratives']/results[yr]['marg_narratives'])
    return [x,y]

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
plt.ylabel('Ratio of Directly Mainstreamed Narratives to All Marginal Narratives')
plt.title('Proportion Narratives Mainstreamed over time ')
plt.show()