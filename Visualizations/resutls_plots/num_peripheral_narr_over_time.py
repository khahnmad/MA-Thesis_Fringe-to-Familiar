"""
COMPLETE
"""
import universal_functions as uf
import matplotlib.pyplot as plt
from Results.locations import *
# x axis = year
# y axis = # marg narratives per pipeline

def get_data(direct_folder):
    results = {}
    for file in direct_folder:
        data = uf.import_json_content(file)

        for ds in data.keys():
            year = ds[-4:]
            if year not in results.keys():
                results[year] = 0

            for t in data[ds].keys():
                num_main_narratives = len(data[ds][t])
                results[year] += num_main_narratives

    x, y = [],[]
    for yr in results.keys():
        x.append(yr)
        y.append(results[yr])
    return [x,y]


x_y_97_20 = get_data(periph_narr_97_20)
x_y_97_30 = get_data(periph_narr_97_30)
x_y_98_20 = get_data(periph_narr_98_20)
x_y_98_30 = get_data(periph_narr_98_30)
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
plt.ylabel('Number of Peripherally Mainstreamed Narratives')
plt.title('Number of Peripherally Mainstreamed Narratives over time ')
plt.show()