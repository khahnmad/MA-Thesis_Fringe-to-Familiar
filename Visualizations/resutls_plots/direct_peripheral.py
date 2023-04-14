import universal_functions as uf
from collections import Counter
import matplotlib.pyplot as plt

partisanships = ["FarRight","Right","CenterRight","Center","CenterLeft","Left","FarLeft"]

def plot_each_marginal_narrative(all_narr_folder):
    for file in all_narr_folder:
        data = uf.import_json_content(file)
        ds_name = list(data.keys())[0]
        data = data[ds_name]

        marg_matches = {}
        for t in data.keys():
            for marg_cluster_id in data[t].keys():
                direct_matches, periph_matches = [], []
                for fs_ds in data[t][marg_cluster_id].keys():
                    for fs_cluster_id in data[t][marg_cluster_id][fs_ds].keys():
                        direct_matches.append(fs_ds)

                        for ss_ds in data[t][marg_cluster_id][fs_ds][fs_cluster_id].keys():
                            for ss_cluster_id in data[t][marg_cluster_id][fs_ds][fs_cluster_id][ss_ds]:
                                periph_matches.append(ss_ds)
                if len(direct_matches) > 0:
                    marg_matches[f"{t}_{marg_cluster_id}"] = [direct_matches, periph_matches]

        for t_cluster_id in marg_matches.keys():
            direct_counter = Counter([x[:-7] for x in marg_matches[t_cluster_id][0]])
            direct_y, x = [], []
            for i in partisanships:
                x.append(i)
                direct_y.append(direct_counter[i])

            periph_counter = Counter([x[:-7] for x in marg_matches[t_cluster_id][1]])
            periph_y = []
            for i in partisanships:
                periph_y.append(periph_counter[i])

            plt.plot(x, direct_y)
            plt.plot(x, periph_y)
            plt.show()

def plot_each_topic_summary(all_narr_folder):
    for file in all_narr_folder:
        data = uf.import_json_content(file)
        ds_name = list(data.keys())[0]
        data = data[ds_name]

        topic_matches = {}
        for t in data.keys():
            direct_matches, periph_matches = [], []
            for marg_cluster_id in data[t].keys():

                for fs_ds in data[t][marg_cluster_id].keys():
                    for fs_cluster_id in data[t][marg_cluster_id][fs_ds].keys():
                        direct_matches.append(fs_ds)

                        for ss_ds in data[t][marg_cluster_id][fs_ds][fs_cluster_id].keys():
                            for ss_cluster_id in data[t][marg_cluster_id][fs_ds][fs_cluster_id][ss_ds]:
                                periph_matches.append(ss_ds)
            if len(direct_matches) > 0:
                topic_matches[t] = [direct_matches, periph_matches]

        for t in topic_matches.keys():
            direct_counter = Counter([x[:-7] for x in topic_matches[t][0]])
            direct_y, x = [], []
            for i in partisanships:
                x.append(i)
                direct_y.append(direct_counter[i])

            periph_counter = Counter([x[:-7] for x in topic_matches[t][1]])
            periph_y = []
            for i in partisanships:
                periph_y.append(periph_counter[i])

            plt.plot(x, direct_y, label='Directly Mainstreamed')
            plt.plot(x, periph_y, label='Peripherally Mainstreamed')
            plt.xlabel('Partisanship')
            plt.ylabel('Number of Mainstreamed Narratives')
            plt.legend()
            plt.title(f"{ds_name}, {t}")
            plt.show()

def plot_each_year_summary(all_narr_folder, title):
    year_matches = {}
    for file in all_narr_folder:
        data = uf.import_json_content(file)
        ds_name = list(data.keys())[0]
        data = data[ds_name]
        year = ds_name[-4:]

        all_direct_matches, all_periph_matches = [], []
        for t in data.keys():
            for marg_cluster_id in data[t].keys():
                for fs_ds in data[t][marg_cluster_id].keys():
                    for fs_cluster_id in data[t][marg_cluster_id][fs_ds].keys():
                        all_direct_matches.append(fs_ds)

                        for ss_ds in data[t][marg_cluster_id][fs_ds][fs_cluster_id].keys():
                            for ss_cluster_id in data[t][marg_cluster_id][fs_ds][fs_cluster_id][ss_ds]:
                                all_periph_matches.append(ss_ds)


        direct_loc = file.replace('all_marginal_narr_matches','direct_mainstreamed_narratives')
        direct_data = uf.import_json_content(direct_loc)

        direct_matches = []
        for d_t in direct_data[ds_name].keys():
            for d_marg_cluster_id in direct_data[ds_name][d_t].keys():
                for d_fs_ds in direct_data[ds_name][d_t][d_marg_cluster_id].keys():
                    for d_fs_cluster_id in direct_data[ds_name][d_t][d_marg_cluster_id][d_fs_ds].keys():
                        direct_matches.append(d_fs_ds)

        periph_loc = direct_loc.replace('direct','periph')
        periph_data = uf.import_json_content(periph_loc)

        periph_matches = []
        for p_t in periph_data[ds_name].keys():
            for p_marg_cluster_id in periph_data[ds_name][p_t].keys():
                for p_fs_ds in periph_data[ds_name][p_t][p_marg_cluster_id].keys():
                    for p_fs_cluster_id in periph_data[ds_name][p_t][p_marg_cluster_id][p_fs_ds].keys():
                        for p_ss_ds in periph_data[ds_name][p_t][p_marg_cluster_id][p_fs_ds][p_fs_cluster_id].keys():
                            for p_ss_cluster_id in periph_data[ds_name][p_t][p_marg_cluster_id][p_fs_ds][p_fs_cluster_id][p_ss_ds]:
                                periph_matches.append(p_ss_ds)

        if len(all_direct_matches) > 0:
            year_matches[year] = [all_direct_matches, all_periph_matches, direct_matches, periph_matches]

    for t in year_matches.keys():
        if "0.2" in year_matches[t][0][0] or "0.3" in year_matches[t][0][0]:
            division_pt = -11
        else:
            division_pt = -7
        direct_counter = Counter([x[:division_pt] for x in year_matches[t][0]])
        direct_y, x = [], []
        for i in partisanships:
            x.append(i)
            direct_y.append(direct_counter[i])

        periph_counter = Counter([x[:division_pt] for x in year_matches[t][1]])
        periph_y = []
        for i in partisanships:
            periph_y.append(periph_counter[i])

        m_direct_counter = Counter([x[:division_pt] for x in year_matches[t][2]])
        m_direct_y, x = [], []
        for i in partisanships:
            x.append(i)
            m_direct_y.append(m_direct_counter[i])

        m_periph_counter = Counter([x[:division_pt] for x in year_matches[t][3]])
        m_periph_y = []
        for i in partisanships:
            m_periph_y.append(m_periph_counter[i])

        plt.plot(x, direct_y, label='Direct Matches')
        plt.plot(x, periph_y, label='Peripheral Matches')
        plt.plot(x, m_direct_y, label='Mainstreamed Direct Matches')
        plt.plot(x, m_periph_y, label='Mainstreamed Peripheral Matches')
        plt.legend()
        plt.xlabel('Partisanship')
        plt.ylabel('Number of Narrative Instances')
        plt.title(f"{title}, {t}: Number of Narrative Instances in each Partisanship ")
        plt.show()


def plot_all_peripherals(all_narr_folder, title):
    marg_matches = {}

    for file in all_narr_folder:
        data = uf.import_json_content(file)
        ds_name = list(data.keys())[0]
        data = data[ds_name]

        for t in data.keys():
            for marg_cluster_id in data[t].keys():
                periph_matches = []
                for fs_ds in data[t][marg_cluster_id].keys():
                    for fs_cluster_id in data[t][marg_cluster_id][fs_ds].keys():
                        for ss_ds in data[t][marg_cluster_id][fs_ds][fs_cluster_id].keys():
                            for ss_cluster_id in data[t][marg_cluster_id][fs_ds][fs_cluster_id][ss_ds]:
                                periph_matches.append(ss_ds)
                if len(periph_matches) > 0:
                    marg_matches[f"{ds_name}_{t}_{marg_cluster_id}"] = periph_matches
    # plot many peripherals, groupt by topic  and dataset name
    complete = []
    for t_cluster_id in marg_matches.keys():
        # get keys from the same topic & dataset
        elts = t_cluster_id.split('_')
        if f"{elts[0]}_{elts[1]}_{elts[2]}" in complete:
            continue
        if "0.2" in  marg_matches[t_cluster_id][0] or "0.3" in marg_matches[t_cluster_id][0]:
            division_point = -11
        else:
            division_point = -7
        complete.append( f"{elts[0]}_{elts[1]}_{elts[2]}")
        corresponding_keys = [k for k in marg_matches.keys() if elts[0] in k and elts[1] in k and elts[2] in k]
        dict_subset = {k:marg_matches[k] for k in corresponding_keys}

        for k in dict_subset.keys():
            periph_counter = Counter([x[:division_point] for x in dict_subset[k]])
            periph_y, x = [], []
            for i in partisanships:
                x.append(i)
                periph_y.append(periph_counter[i])
            plt.plot(x, periph_y)
        plt.title(f"{title}: {elts[0]}_{elts[1]}_{elts[2]}")
        plt.show()


    # # plot every indivual peripheral
    # for t_cluster_id in marg_matches.keys():
    #
    #     periph_counter = Counter([x[:-7] for x in marg_matches[t_cluster_id]])
    #     periph_y, x = [],[]
    #     for i in partisanships:
    #         x.append(i)
    #         periph_y.append(periph_counter[i])
    #
    #     plt.plot(x, periph_y)
    #     plt.title(f"{title}: {t_cluster_id}")
    #     plt.show()

def plot_peripheral_topic_summary(all_narr_folder):
    marg_matches = {}

    for file in all_narr_folder:
        data = uf.import_json_content(file)
        ds_name = list(data.keys())[0]
        data = data[ds_name]

        for t in data.keys():
            periph_matches = []
            for marg_cluster_id in data[t].keys():

                for fs_ds in data[t][marg_cluster_id].keys():
                    for fs_cluster_id in data[t][marg_cluster_id][fs_ds].keys():
                        for ss_ds in data[t][marg_cluster_id][fs_ds][fs_cluster_id].keys():
                            for ss_cluster_id in data[t][marg_cluster_id][fs_ds][fs_cluster_id][ss_ds]:
                                periph_matches.append(ss_ds)
            if len(periph_matches) > 0:
                marg_matches[t] = periph_matches

    for t in marg_matches.keys():

        periph_counter = Counter([x[:-7] for x in marg_matches[t]])
        periph_y, x = [], []
        for i in partisanships:
            x.append(i)
            periph_y.append(periph_counter[i])

        plt.plot(x, periph_y)
    plt.show()

cosine_97_20_all_narr = [x for x in uf.get_files_from_folder(f"{uf.thesis_location}Tracking\\LowClass_Threshold","json") if '0.2' in x and 'emojj' not in x and 'all_marginal' in x ]
cosine_97_30_all_narr = [x for x in uf.get_files_from_folder(f"{uf.thesis_location}Tracking\\LowClass_Threshold","json") if '0.3' in x and 'emojj' not in x and 'all_marginal' in x]

cosine_98_20_all_narr = [x for x in uf.get_files_from_folder(f"{uf.thesis_location}Tracking\\HighClass_Threshold","json") if '0.2' in x and 'emojj' not in x and 'all_marginal' in x]
cosine_98_30_all_narr = [x for x in uf.get_files_from_folder(f"{uf.thesis_location}Tracking\\HighClass_Threshold","json") if '0.3' in x and 'emojj' not in x and 'all_marginal' in x]



# plot_each_marginal_narrative(cosine_97_20_all_narr)
# plot_each_topic_summary(cosine_97_20_all_narr)

# plot_each_year_summary(cosine_97_20_all_narr, "Low Clusters, Low Classification")
# plot_each_year_summary(cosine_97_30_all_narr, "High Clusters, Low Classification")
# plot_each_year_summary(cosine_98_20_all_narr, "Low Clusters, High Classification")
# plot_each_year_summary(cosine_98_30_all_narr, "High Clusters, High Classification")


# plot_all_peripherals(cosine_97_20_all_narr, "Low Clusters, Low Classification")
# plot_all_peripherals(cosine_97_30_all_narr, "High Clusters, Low Classification")
plot_all_peripherals(cosine_98_20_all_narr, "Low Clusters, High Classification")
plot_all_peripherals(cosine_98_30_all_narr, "High Clusters, High Classification")
# plot_peripheral_topic_summary(cosine_97_20_all_narr)