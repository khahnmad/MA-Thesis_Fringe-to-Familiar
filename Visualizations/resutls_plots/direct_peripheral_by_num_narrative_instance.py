from Results.locations import *
from collections import Counter
import matplotlib.pyplot as plt

# X axis: year
# y axis: number of narrative instances
# groupings: direct & peripheral
def get_year(ds_name):
    if ds_name.endswith('0.2') or ds_name.endswith('0.3'):
        year =  ds_name.split('-')[-1][:-4]
    else:
        year = ds_name.split('-')[-1]
    return int(year)

def get_direct_matches_per_year(direct_folder):
    # Get the number of direct matches per year for every mainstreamed narratives
    years = [2016,2017,2018,2019,2020]
    direct_y =[]
    for file in direct_folder:
        data = uf.import_json_content(file)
        ds_name = list(data.keys())[0]

        for t in data[ds_name].keys():
            for marg_cluster_id in data[ds_name][t].keys():
                y= []
                narrative = [get_year(ds_name)]
                # if cluster_id not in fs_main[ds_name][t]:
                #     continue
                for fs_ds in data[ds_name][t][marg_cluster_id].keys():
                    year = get_year(fs_ds)
                    narrative.append(year)
                counter = Counter(narrative)
                for year in years:
                    y.append(counter[year])
                # direct_x.append(x)
                direct_y.append(y)
    return years, direct_y

# PLOTTING
def plot_many_lines(x,Y,title, x_label, y_label):
    for y in Y:
        plt.plot(x,y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()

def plot_many_lines_w_legend(x,Y,title, x_label, y_label, labels):
    for i in range(len(Y)):
        plt.plot(x,Y[i], label=labels[i])
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.title(title)
    plt.show()

def plot_one_line(x,y, title, x_label, y_label):
    plt.plot(x,y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()

def get_peripheral_matches_per_year(fs_folder, ss_folder, ss_main, fs_main):
    years = [2016, 2017, 2018, 2019, 2020]
    direct_y = []
    for file in ss_folder:
        data = uf.import_json_content(file)
        ds_name = uf.get_dataset_id(file)
        cluster_type = file.split('_')[-1][:-5]

        # fs_file = [x for x in fs_folder if f"\\{ds_name}_{cluster_type}" in x]
        # fs_data = uf.import_json_content(fs_file[0])
        for t in data.keys():
            for ds in data[t].keys():
                for cluster_id in data[t][ds].keys():
                    if cluster_id not in fs_main[ds_name][t]:
                        continue
                    y = []
                    narrative = []
                    for elt in data[t][ds][cluster_id]:
                        year = get_year(elt[0])
                        narrative.append(year)
                    counter = Counter(narrative)
                    for year in years:
                        y.append(counter[year])
                    # direct_x.append(x)
                    direct_y.append(y)

                    print('check')
    return


def plot_mainstreamed_narr_direct_instances(direct_folder, title):
    # Plot every mainstreamed narrative's direct instances
    x, Y = get_direct_matches_per_year(direct_folder)
    plot_many_lines(x,Y, f"{title}:Number of Direct Instance Matches per Year for each Mainstreamed Narrative","Year",
                    "Number of Direct Instances Matches")

    # Plot summary of the direct matches
    sum_y = []
    for i in range(len(Y[0])):
        sum_y.append(sum([x[i] for x in Y]))
    plot_one_line(x, sum_y, title=f"{title}: Sum of Direct Instance Matches per Year for all Mainstreamed Narratives",
                  x_label="Year",y_label="Number of Direct Instance Matches")

    # Plot average of the direct matches
    avg_y = []
    for i in range(len(Y[0])):
        avg_y.append(sum([x[i] for x in Y])/len([x[i] for x in Y]))
    plot_one_line(x, avg_y, title=f"{title}: Average Number of Direct Instance Matches per Year for all Mainstreamed Narratives",
                  x_label="Year", y_label="Number of Direct Instance Matches")

    # Plot sum and average on the same plot

    plot_many_lines(x,[sum_y,avg_y],x_label='Year',y_label="Num Direct Instance Matches",
                    title=f"{title}: Sum and Average # Direct INstance Matches per Year for all mainstreamed narratives")


def plot_mainstreamed_narr_peripheral_instances(fs_main, ss_folder, ss_main,title):
    # Plot every mainstreamed narrative's direct instances
    x, Y = get_peripheral_matches_per_year(ss_main=ss_main,ss_folder=ss_folder, fs_folder=fs_main)
    plot_many_lines(x,Y, f"{title}:Number of Peripheral Matches per Year for each Mainstreamed Narrative","Year",
                    "Number of Peripheral Instances Matches")

    # Plot summary of the direct matches
    y = []
    for i in range(len(Y[0])):
        y.append(sum([x[i] for x in Y]))
    plot_one_line(x, y, title=f"{title}: Sum of Peripheral Instance Matches per Year for all Mainstreamed Narratives",x_label="Year",y_label="Number of Peripheral Instance Matches")


def plot_direct_peripheral_instances_for_mainstreamed_narratives(fs_main, fs_folder,ss_folder, ss_main):
    x, Y = get_direct_matches_per_year(fs_main, fs_folder)
    sum_y = []
    for i in range(len(Y[0])):
        sum_y.append(sum([x[i] for x in Y]))

    x,Y = get_peripheral_matches_per_year(fs_folder,ss_folder, ss_main)


def plot_num_direct_matches_per_year_by_pipeline_modification():
    labels = ["Fewer Cluster, Lower Class Threshold", "More Cluster, Lower Class Threshold",
              "Fewer Cluster, High Class Threshold", "More Cluster, High Class Threshold"]
    folders = [dir_narr_97_20, dir_narr_97_30, dir_narr_98_20, dir_narr_98_30]
    avg_Ys, sum_Ys = [],[]
    for i in range(len(folders)):
        direct_folder = folders[i]

        x, Y = get_direct_matches_per_year(direct_folder)

        # Get average of the direct matches
        avg_y = []
        for i in range(len(Y[0])):
            avg_y.append(sum([x[i] for x in Y]) / len([x[i] for x in Y]))
        avg_Ys.append(avg_y)

        # Get sum of direct matches
        sum_y = []
        for i in range(len(Y[0])):
            sum_y.append(sum([x[i] for x in Y]))
        sum_Ys.append(sum_y)

    x =  [2016,2017,2018,2019,2020]

    plot_many_lines_w_legend(x, sum_Ys, x_label='Year', y_label="Num Direct Instance Matches", labels=labels,
                    title=f"Sum of the # of Direct Instance Matches per Year for all mainstreamed narratives, by pipeline modification")
    plot_many_lines_w_legend(x, avg_Ys, x_label='Year', y_label="Num Direct Instance Matches", labels=labels,
                             title=f"Average of the # of Direct Instance Matches per Year for all mainstreamed narratives, by pipeline modification")


# plot_mainstreamed_narr_direct_instances(dir_narr_97_20, "Fewer Cluster, Lower Class Threshold")
# plot_mainstreamed_narr_direct_instances(dir_narr_97_30, "More Cluster, Lower Class Threshold")
# plot_mainstreamed_narr_direct_instances(dir_narr_98_20, "Fewer Cluster, High Class Threshold")
# plot_mainstreamed_narr_direct_instances(dir_narr_98_30, "More Cluster, High Class Threshold")
#
#
# plot_mainstreamed_narr_peripheral_instances(fs_main=fs_nosent_97_20_main,ss_main=ss_nosent_97_20_main, ss_folder=ss_97_20_nosent,
#                                             title="Fewer Cluster, Lower Class Threshold")
#
# plot_direct_peripheral_instances_for_mainstreamed_narratives(fs_main=fs_nosent_97_20_main,ss_main=ss_nosent_97_20_main,
#                                                              ss_folder=ss_97_20_nosent,fs_folder=fs_97_20_nosent)

"""COMPLETE"""
plot_num_direct_matches_per_year_by_pipeline_modification()