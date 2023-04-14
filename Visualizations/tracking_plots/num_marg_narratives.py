import universal_functions as uf
import matplotlib.pyplot as plt
import pandas as pd

def plot_num_marg_narratives_by_topic(narr_folder, title):
    topic_marg = {}
    for file in narr_folder:
        data = uf.import_json_content(file)
        ds_name = list(data.keys())[0]
        data = data[ds_name]

        for t in data.keys():
            if t not in topic_marg.keys():
                topic_marg[t] = 0
            marg_narr = len(data[t])
            topic_marg[t] += marg_narr

    x = list(topic_marg.keys())
    y = list(topic_marg.values())

    plt.bar(x, y)
    plt.title(f"{title}: Number of Far Right Marginal Narratives per Topic")
    plt.xlabel("Topic")
    plt.ylabel("Number of Marginal Narratives")
    plt.show()

cosine_97_20_all_narr = [x for x in uf.get_files_from_folder(f"{uf.thesis_location}Tracking\\LowClass_Threshold","json") if '0.2' in x and 'emojj' not in x]
cosine_97_30_all_narr = [x for x in uf.get_files_from_folder(f"{uf.thesis_location}Tracking\\LowClass_Threshold","json") if '0.3' in x and 'emojj' not in x]

cosine_98_20_all_narr = [x for x in uf.get_files_from_folder(f"{uf.thesis_location}Tracking\\HighClass_Threshold","json") if '0.2' in x and 'emojj' not in x]
cosine_98_30_all_narr = [x for x in uf.get_files_from_folder(f"{uf.thesis_location}Tracking\\HighClass_Threshold","json") if '0.3' in x and 'emojj' not in x]

# plot_num_marg_narratives_by_topic(cosine_97_20_all_narr,"Few Clusters, Low Classification Threshold")
# plot_num_marg_narratives_by_topic(cosine_97_30_all_narr,"More Clusters, Low Classification Threshold")
# plot_num_marg_narratives_by_topic(cosine_98_20_all_narr,"Few Clusters, High Classification Threshold")
# plot_num_marg_narratives_by_topic(cosine_98_30_all_narr,"More Clusters, High Classification Threshold")

def get_file_x_y(narr_folder):
    topic_marg = {}
    for file in narr_folder:
        data = uf.import_json_content(file)
        ds_name = list(data.keys())[0]
        data = data[ds_name]

        for t in ["Immigration", "Islamophobia","Anti-semitism","Transphobia"]:
            if t not in topic_marg.keys():
                topic_marg[t] = 0
            try:
                marg_narr = len(data[t])
            except KeyError:
                marg_narr =0
            topic_marg[t] += marg_narr

    # x = list(topic_marg.keys())
    y = list(topic_marg.values())
    return y

def get_file_marg_direct_peripheral(narr_folder):

    num_marg, num_direct, num_periph =0,0,0
    for file in narr_folder:
        data = uf.import_json_content(file)
        ds_name = list(data.keys())[0]
        data = data[ds_name]

        for t in data.keys():
            num_marg += len(data[t])

            for marg_cluster_id in data[t].keys():
                for fs_ds in data[t][marg_cluster_id].keys():
                    num_direct+= len(data[t][marg_cluster_id][fs_ds])

                    for fs_cluster_id in data[t][marg_cluster_id][fs_ds].keys():
                        for ss_ds in data[t][marg_cluster_id][fs_ds][fs_cluster_id].keys():
                            num_periph += len(data[t][marg_cluster_id][fs_ds][fs_cluster_id][ss_ds])

    return [num_marg, num_direct, num_periph]


def plot_num_marg_narratives():
    cols = ["Parameters","Immigration", "Islamophobia","Anti-semitism","Transphobia"]

    plottable = []
    plottable.append(["Low Clustering, Low Threshold"]+get_file_x_y(cosine_97_20_all_narr))
    plottable.append(["High Clustering, Low Threshold"]+get_file_x_y(cosine_97_30_all_narr))
    plottable.append(["Low Clustering, High Threshold"]+get_file_x_y(cosine_98_20_all_narr))
    plottable.append(["High Clustering, High Threshold"]+get_file_x_y(cosine_98_30_all_narr))

    df = pd.DataFrame(plottable, columns=cols)


    # plotting graph
    fig = df.plot(x="Parameters", y=["Immigration", "Islamophobia","Anti-semitism","Transphobia"], kind="bar")
    plt.tight_layout()
    plt.ylabel("Number of Marginal Narratives")
    plt.xticks(rotation=45)
    plt.show()


def plot_num_marg_direct_periperal_narratives():
    cols = ["Parameters", "Marginal", "Direct", "Peripheral"]

    plottable = []
    plottable.append(["Low Clustering, Low Threshold"] + get_file_marg_direct_peripheral(cosine_97_20_all_narr))
    plottable.append(["High Clustering, Low Threshold"] + get_file_marg_direct_peripheral(cosine_97_30_all_narr))
    plottable.append(["Low Clustering, High Threshold"] + get_file_marg_direct_peripheral(cosine_98_20_all_narr))
    plottable.append(["High Clustering, High Threshold"] + get_file_marg_direct_peripheral(cosine_98_30_all_narr))

    df = pd.DataFrame(plottable, columns=cols)

    # plotting graph
    fig = df.plot(x="Parameters", y=[ "Marginal", "Direct", "Peripheral"], kind="bar")
    plt.tight_layout()
    plt.ylabel("Number of Narrative Instances")
    plt.xticks(rotation=45)
    plt.show()

# plot_num_marg_narratives()
plot_num_marg_direct_periperal_narratives()