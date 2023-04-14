import universal_functions as uf
from collections import Counter

def get_marginal_NEs(file, topic, part=None):
    named_entities = []

    marg_data = uf.import_json_content(file)
    direct_data = uf.import_json_content(
        file.replace("all_marginal_narr_matches", "direct_mainstreamed_narratives"))
    periph_data = uf.import_json_content(
        file.replace("all_marginal_narr_matches", "periph_mainstreamed_narratives"))

    for k in marg_data.keys():
        try:
            for marg_cluster_id in marg_data[k][topic].keys():
                if marg_cluster_id in direct_data[k][topic].keys() or periph_data[k][topic].keys():
                    if part:
                        if k.startswith(part):
                            named_entities += uf.remove_duplicates(
                                [x[0] for x in marg_data[k][topic][marg_cluster_id]])
                    else:
                        named_entities += uf.remove_duplicates([x[0] for x in marg_data[k][topic][marg_cluster_id]])
        except KeyError:
            continue
    return named_entities

def get_NEs(files, topic):
    if 'marginal' in files[0]:
        # Need the marg, direct, & periph
        named_entities = get_marginal_NEs(files, topic)
    else:
        named_entities = []
        for file in files:
            data = uf.import_json_content(file)

            for k in data.keys():
                try:
                    for marg_cluster_id in data[k][topic].keys():
                        for fs_ds in data[k][topic][marg_cluster_id].keys():
                            for fs_cluster_id in data[k][topic][marg_cluster_id][fs_ds].keys():
                                if "direct" in file:
                                    named_entities += uf.remove_duplicates([x[0] for x in data[k][topic][marg_cluster_id][fs_ds][fs_cluster_id]])
                                    continue

                                for ss_ds in data[k][topic][marg_cluster_id][fs_ds][fs_cluster_id].keys():
                                    for ss_cluster_id in data[k][topic][marg_cluster_id][fs_ds][fs_cluster_id][ss_ds]:
                                        named_entities += uf.remove_duplicates([x[0] for x in ss_cluster_id])

                except KeyError:
                    continue
    return named_entities

def get_NEs_by_part(files, topic, part):
    named_entities = []
    for file in files:
        if 'marginal' in file:
            # Need the marg, direct, & periph
            named_entities += get_marginal_NEs(file, topic, part)
        else:

            data = uf.import_json_content(file)

            for k in data.keys():
                try:
                    for marg_cluster_id in data[k][topic].keys():
                        for fs_ds in data[k][topic][marg_cluster_id].keys():
                            for fs_cluster_id in data[k][topic][marg_cluster_id][fs_ds].keys():
                                if "direct" in file:
                                    if fs_ds.startswith(part):
                                        named_entities += uf.remove_duplicates([x[0] for x in data[k][topic][marg_cluster_id][fs_ds][fs_cluster_id]])
                                    continue

                                for ss_ds in data[k][topic][marg_cluster_id][fs_ds][fs_cluster_id].keys():
                                    if ss_ds.startswith(part):
                                        for ss_cluster_id in data[k][topic][marg_cluster_id][fs_ds][fs_cluster_id][ss_ds]:
                                            named_entities += uf.remove_duplicates([x[0] for x in ss_cluster_id])

                except KeyError:
                    continue
    return named_entities


def find_unique(group_a, group_b):
    unique = []
    for item in group_a:
        if item not in group_b:
            unique.append(item)
    return unique


def find_most_common(group):
    counter = Counter(group).most_common(5)
    # mc = []
    # for c in counter.keys():
    #     if counter[c] > 1:
    #         mc.append((c, counter[c]))
    return list(counter)

def create_grouping(group, title):
    row = [['',title,'']]
    for x in group:
        row.append(['','',x[0],x[1]])
    return row

def create_table(topic, marginal, direct, peripheral, table):
    table += [[topic,"",""]]
    table += create_grouping(marginal, 'Marginal')
    table += create_grouping(direct, 'Direct')
    table += create_grouping(peripheral, 'Peripheral')
    return table

def get_unique_NEs_by_step():
    for class_type in ["97","98"]: # Iterate through class type
        for cluster_type in ["0.2","0.3"]: # Iterate through cluster type
            loc = f"{uf.thesis_location}Results\\rq_2\\no_sent\\cosine_{class_type}\\"
            marg_files = [x for x in uf.get_files_from_folder(loc,'json') if "marginal_NEs" in x and cluster_type in x]
            dir_files = [x for x in uf.get_files_from_folder(loc, 'json') if "direct_NEs" in x and cluster_type in x]
            periph_files = [x for x in uf.get_files_from_folder(loc, 'json') if "periph_NEs" in x and cluster_type in x]

            unique_imp_table, imp_table = [],[]
            for t in ["Immigration","Islamophobia","Anti-semitism","Transphobia"]: # Iterate through topics
                marg_NEs = get_NEs(marg_files, t)
                direct_NEs = get_NEs(dir_files, t)
                periph_NEs = get_NEs(periph_files, t)

                # Find any word that appears uniquely in each category
                marg_unique = find_unique(marg_NEs, direct_NEs+periph_NEs)
                dir_unique = find_unique(direct_NEs, marg_NEs + periph_NEs)
                periph_unique = find_unique(periph_NEs, direct_NEs + marg_NEs)

                # Find most important unique
                marg_imp_unique = find_most_common(marg_unique)
                dir_imp_unique = find_most_common(dir_unique)
                periph_imp_unique = find_most_common(periph_unique)
                create_table(t, marg_imp_unique, dir_imp_unique, periph_imp_unique, unique_imp_table)

                # Find most important non unique
                marg_imp = find_most_common(marg_NEs)
                dir_imp = find_most_common(direct_NEs)
                periph_imp = find_most_common(periph_NEs)
                create_table(t, marg_imp, dir_imp, periph_imp, imp_table)

            uf.export_nested_list(f"{loc}{cluster_type}_Unique_Important.csv",unique_imp_table)
            uf.export_nested_list(f"{loc}{cluster_type}_NonUnique_Important.csv", imp_table)

def get_unique_NEs_by_partisanship():
    for class_type in ["97","98"]: # Iterate through class type
        for cluster_type in ["0.2","0.3"]: # Iterate through cluster type
            loc = f"{uf.thesis_location}Results\\rq_2\\no_sent\\cosine_{class_type}\\"
            marg_files = [x for x in uf.get_files_from_folder(loc,'json') if "marginal_NEs" in x and cluster_type in x]
            dir_files = [x for x in uf.get_files_from_folder(loc, 'json') if "direct_NEs" in x and cluster_type in x]
            periph_files = [x for x in uf.get_files_from_folder(loc, 'json') if "periph_NEs" in x and cluster_type in x]
            all_files = marg_files + dir_files + periph_files

            unique_table, nonunique_table = [],[]
            for t in ["Immigration","Islamophobia","Anti-semitism","Transphobia"]: # Iterate through topics
                unique_table.append([t,"",''])
                nonunique_table.append([t,"",''])

                results = {"Right":[],"Center":[],"Left":[]}
                for p in ["FarRight","Right"]:
                    results["Right"] += get_NEs_by_part(all_files, t, p)
                for pp in ["CenterRight","Center","CenterLeft"]:
                    results["Center"] += get_NEs_by_part(all_files, t, pp)
                for ppp in ["Left","FarLeft"]:
                    results["Left"] +=  get_NEs_by_part(all_files, t, ppp)
                unique_results = {}
                for k in results.keys():
                    unique_table.append(["",k,"",""])
                    remaining = uf.flatten_list([results[key] for key in results.keys() if key!=k])
                    unique=find_unique(results[k], remaining)
                    unique_results[k] = find_most_common(unique)
                    for elt in unique_results[k]:
                        unique_table.append(["","",elt[0], elt[1]])

                nonunique_results = {}
                for k in results.keys():
                    nonunique_table.append(["",k,"",""])
                    nonunique_results[k] = find_most_common(results[k])
                    for elt in nonunique_results[k]:
                        nonunique_table.append(["","",elt[0], elt[1]])
            uf.export_nested_list(f"{loc}{cluster_type}_Unique_Important_partisanships.csv", unique_table)
            uf.export_nested_list(f"{loc}{cluster_type}_NonUnique_Important_partisanships.csv", nonunique_table)


# get_unique_NEs_by_step()
get_unique_NEs_by_partisanship()