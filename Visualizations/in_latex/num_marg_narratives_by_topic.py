"""
COMPLETE
"""
import universal_functions as uf
import matplotlib.pyplot as plt
from Results.locations import *
# x axis = year
# y axis = # marg narratives per pipeline

def get_data(marg_folder):
    results = {}
    for file in marg_folder:
        data = uf.import_json_content(file)

        for ds in data.keys():
            for t in data[ds].keys():
                if t not in results.keys():
                    results[t] = 0
                num_main_narratives = len(data[ds][t])
                results[t] += num_main_narratives

    x, y = [],[]
    for topic in results.keys():
        x.append(topic)
        y.append(results[topic])
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
    plt.scatter(row[0], row[1],  label=labels[i])
plt.legend()
plt.xlabel('Topic')
plt.ylabel('Number of Marginal Narratives')
plt.title('Number of Marginal Narratives by Topic and Pipeline Modification')
plt.show()