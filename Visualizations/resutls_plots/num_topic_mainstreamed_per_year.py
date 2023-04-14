
import universal_functions as uf
import matplotlib.pyplot as plt
from Results.locations import *
# x axis = year
# y axis = # narratives mainstreamed per topic

def get_data(direct_folder, topic):
    results = {}
    for file in direct_folder:
        data = uf.import_json_content(file)

        for ds in data.keys():
            year = ds[-4:]
            if year not in results.keys():
                results[year] = 0

            try:
                num_main_narratives = len(data[ds][topic])
            except KeyError:
                num_main_narratives = 0
            results[year] += num_main_narratives

    x, y = [],[]
    for yr in results.keys():
        x.append(yr)
        y.append(results[yr])
    return [x,y]


def plot_narratives_per_topic(topic):
    x_y_97_20 = get_data(dir_narr_97_20,topic)
    x_y_97_30 = get_data(dir_narr_97_30,topic)
    x_y_98_20 = get_data(dir_narr_98_20, topic)
    x_y_98_30 = get_data(dir_narr_98_30, topic)
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
    plt.ylabel('Number of Mainstreamed Narratives')
    plt.title(f'Number of Maintreamed {topic} Narratives over time ')
    plt.show()

for t in ["Immigration",'Islamophobia','Transphobia',"Anti-semitism"]:
    plot_narratives_per_topic(t)