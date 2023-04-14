import universal_functions as uf
# from Results.locations import *
# from collections import Counter

# GLOBAL

cosine_97 = uf.repo_loc / 'Reconstruction_Phase/Tracking/LowClass_Threshold'
cosine_98 = uf.repo_loc / 'Reconstruction_Phase/Tracking/HighClass_Threshold'

# FUNCTIONS

def get_marginal_narratives(marg_narr_loc, narratives, marg_dataset):
    marg_narr = uf.import_json_content(marg_narr_loc)

    narratives[marg_dataset] = {}  # Todo: Should include cluster type

    for t in marg_narr.keys():
        narratives[marg_dataset][t] = {}
        for marg_cluster_id in marg_narr[t]:
            narratives[marg_dataset][t][str(marg_cluster_id)] = {}
    return narratives


def get_direct_matches(marg_narr_loc, narratives, marg_dataset):
    first_step_loc = marg_narr_loc.replace("Marginal_Narratives", "First_Step_Narratives")
    fs_data = uf.import_json_content(first_step_loc)

    for t in fs_data.keys():
        for marg_cluster_id in fs_data[t].keys():
            for fs_match in fs_data[t][marg_cluster_id]:
                if fs_match[0] not in narratives[marg_dataset][t][marg_cluster_id].keys():
                    narratives[marg_dataset][t][marg_cluster_id][fs_match[0]] = {}
                narratives[marg_dataset][t][marg_cluster_id][fs_match[0]][str(fs_match[1])] = {}
    return narratives


def get_peripheral_matches(marg_step_loc, narratives, marg_dataset):
    ss_loc = marg_step_loc.replace("Marginal", "Second_Step")
    ss_data = uf.import_json_content(ss_loc)

    for t in ss_data.keys():
        for fs_ds in ss_data[t].keys():
            for fs_cluster_id in ss_data[t][fs_ds].keys():
                for ss_match in ss_data[t][fs_ds][fs_cluster_id]:

                    for marg_c_id in narratives[marg_dataset][t].keys():
                        for n_fs_match in narratives[marg_dataset][t][marg_c_id].keys():
                            if n_fs_match == fs_ds:
                                for n_cluster_id in narratives[marg_dataset][t][marg_c_id][n_fs_match].keys():
                                    if n_cluster_id == fs_cluster_id:

                                        if ss_match[0] not in narratives[marg_dataset][t][marg_c_id][n_fs_match][
                                            fs_cluster_id].keys():
                                            narratives[marg_dataset][t][marg_c_id][n_fs_match][fs_cluster_id][
                                                ss_match[0]] = []
                                        narratives[marg_dataset][t][marg_c_id][n_fs_match][fs_cluster_id][
                                            ss_match[0]].append(str(ss_match[1]))
    return narratives


def package_narratives_together(marg_narr_loc):
    narratives = {}
    marg_dataset = uf.get_dataset_id(marg_narr_loc)
    w_marg_narratives = get_marginal_narratives(marg_narr_loc, narratives, marg_dataset)

    w_direct_matches = get_direct_matches(marg_narr_loc, w_marg_narratives, marg_dataset)

    w_peripheral_matches = get_peripheral_matches(marg_narr_loc, w_direct_matches, marg_dataset)
    return w_peripheral_matches


# MAIN FUNCTIONS
def collect_full_sequence(cosine_folder):
    for file in uf.get_files_from_folder(f"{cosine_folder}\\Marginal_Narratives", "json"):
        dataset_name = uf.get_dataset_id(file)
        cluster_type = file.split('_')[-1][:-5]

        narratives = package_narratives_together(file)
        uf.content_json_export(f"{cosine_folder}\\Full_Sequence\\{dataset_name}_{cluster_type}_all_marginal_narr_matches.json",narratives)


def package_just_direct_match_mainstreamed_narratives(narr_match_file):
    export_name = narr_match_file.replace("all_marginal_narr_matches",
                                          "direct_mainstreamed_narratives").replace('Full_Sequence','Direct_Sequence')

    export = {}
    data = uf.import_json_content(narr_match_file)

    for ds_name in data.keys():
        export[ds_name] = {}

        for t in data[ds_name].keys():
            export[ds_name][t] = {}

            for marg_cluster_id in data[ds_name][t].keys():
                direct_matches = []
                for fs_ds in data[ds_name][t][marg_cluster_id].keys():
                    for fs_cluster_id in data[ds_name][t][marg_cluster_id][fs_ds].keys():
                        direct_matches.append(fs_ds)
                if len(direct_matches) == 0:
                    continue
                center = 0
                for c in direct_matches:
                    if "Center" in c:
                        center += 1
                if center/len(direct_matches) >= 0.5:
                    export[ds_name][t][marg_cluster_id] = data[ds_name][t][marg_cluster_id]
    uf.content_json_export(export_name, export)


def package_just_periph_match_mainstreamed_narratives(narr_match_file):
    export_name = narr_match_file.replace("all_marginal_narr_matches",
                                          "periph_mainstreamed_narratives").replace('Full_Sequence',
                                                                                    'Peripheral_Sequence')

    export = {}
    data = uf.import_json_content(narr_match_file)

    for ds_name in data.keys():
        export[ds_name] = {}

        for t in data[ds_name].keys():
            export[ds_name][t] = {}

            for marg_cluster_id in data[ds_name][t].keys():
                periph_matches = []

                for fs_ds in data[ds_name][t][marg_cluster_id].keys():
                    for fs_cluster_id in data[ds_name][t][marg_cluster_id][fs_ds].keys():
                        for ss_ds in data[ds_name][t][marg_cluster_id][fs_ds][fs_cluster_id].keys():
                            for ss_cluster_id in data[ds_name][t][marg_cluster_id][fs_ds][fs_cluster_id][ss_ds]:
                                periph_matches.append(ss_ds)
                if len(periph_matches) == 0:
                    continue
                center = 0
                for c in periph_matches:
                    if "Center" in c:
                        center += 1
                if center/len(periph_matches) >= 0.5:
                    export[ds_name][t][marg_cluster_id] = data[ds_name][t][marg_cluster_id]
                else:
                    print('check')
    uf.content_json_export(export_name, export)


if __name__ == '__main__':

    collect_full_sequence(cosine_97)
    collect_full_sequence(cosine_98)

    full_seq = uf.get_files_from_folder(str(uf.repo_loc / 'Tracking/HighClass_Threshold'),'json') + \
               uf.get_files_from_folder(str(uf.repo_loc / 'Tracking/LowClass_Threshold'),'json')

    for file in full_seq:
        package_just_direct_match_mainstreamed_narratives(file)
        package_just_periph_match_mainstreamed_narratives(file)
