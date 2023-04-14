import universal_functions as uf
from collections import Counter
from scipy.stats import chi2_contingency
from scipy.stats import chi2
import numpy as np

# First create the table for the paper
# Pipeline, Words appearing only in the marginal, # marg narratives it appears in

# rq_no_sent = f"{uf.thesis_location}Results\\rq_2\\no_sent\\"
#
# unique_imp_97_20 = f"{rq_no_sent}cosine_97\\0.2_Unique_Important.csv"
# data = uf.import_csv(unique_imp_97_20)
# print('chek')
keywords = ["Americans", "Christian", "Obama", "America", "Barack Obama", "Christians", "American","Trump","Donald Trump",
            "Muslim","Muslims"]

def calc_chi_square(table):
    stat, p, dof, expected = chi2_contingency(table)
    print('dof=%d' % dof)
    # print(expected)
    # interpret test-statistic
    prob = 0.95
    critical = chi2.ppf(prob, dof)
    print('probability=%.3f, critical=%.3f, stat=%.3f' % (prob, critical, stat))
    if abs(stat) >= critical:
        print('Dependent (reject H0)')
    else:
        print('Independent (fail to reject H0)')
    # interpret p-value
    alpha = 1.0 - prob
    print('significance=%.3f, p=%.3f' % (alpha, p))
    if p <= alpha:
        print('Dependent (reject H0)')
    else:
        print('Independent (fail to reject H0)')


def get_marginal_NEs(file, part=None):
    named_entities = []

    marg_data = uf.import_json_content(file)
    direct_data = uf.import_json_content(
        file.replace("all_marginal_narr_matches", "direct_mainstreamed_narratives"))
    periph_data = uf.import_json_content(
        file.replace("all_marginal_narr_matches", "periph_mainstreamed_narratives"))

    for k in marg_data.keys():
        for topic in marg_data[k].keys():
            for marg_cluster_id in marg_data[k][topic].keys():
                if marg_cluster_id in direct_data[k][topic].keys() or periph_data[k][topic].keys():
                    if part:
                        if k.startswith(part):
                            named_entities += uf.remove_duplicates(
                                [x[0] for x in marg_data[k][topic][marg_cluster_id]])
                    else:
                        named_entities += uf.remove_duplicates([x[0] for x in marg_data[k][topic][marg_cluster_id]])
    return named_entities


def get_NEs(files):
    if 'marginal' in files[0]:
        # Need the marg, direct, & periph
        named_entities = []
        for file in files:
            named_entities+= get_marginal_NEs(file)
    else:
        named_entities = []
        for file in files:
            data = uf.import_json_content(file)

            for k in data.keys():
                for topic in data[k].keys():
                    for marg_cluster_id in data[k][topic].keys():
                        for fs_ds in data[k][topic][marg_cluster_id].keys():
                            for fs_cluster_id in data[k][topic][marg_cluster_id][fs_ds].keys():
                                if "direct" in file:
                                    named_entities += uf.remove_duplicates([x[0] for x in data[k][topic][marg_cluster_id][fs_ds][fs_cluster_id]])
                                    continue

                                for ss_ds in data[k][topic][marg_cluster_id][fs_ds][fs_cluster_id].keys():
                                    for ss_cluster_id in data[k][topic][marg_cluster_id][fs_ds][fs_cluster_id][ss_ds]:
                                        named_entities += uf.remove_duplicates([x[0] for x in ss_cluster_id])
    return named_entities

def find_most_common(group):
    counter = Counter(group).most_common(20)
    # mc = []
    # for c in counter.keys():
    #     if counter[c] > 1:
    #         mc.append((c, counter[c]))
    return list(counter)


def count_keyword_appearances(named_entities, words=keywords):
    counter = Counter(named_entities)
    results = {}
    for word in words:
        results[word] = counter[word]
    return results

def create_table(marg_ents, main_ents, words=keywords):
    table = []
    for word in words:
        table.append([marg_ents[word], main_ents[word]])
    table = list(np.array(table).transpose())
    return table



for class_type in ["97", "98"]:  # Iterate through class type
    for cluster_type in ["0.2", "0.3"]:  # Iterate through cluster type
        loc = f"{uf.thesis_location}Results\\rq_2\\no_sent\\cosine_{class_type}\\"
        marg_files = [x for x in uf.get_files_from_folder(loc, 'json') if "marginal_NEs" in x and cluster_type in x]
        dir_files = [x for x in uf.get_files_from_folder(loc, 'json') if "direct_NEs" in x and cluster_type in x]
        periph_files = [x for x in uf.get_files_from_folder(loc, 'json') if "periph_NEs" in x and cluster_type in x]

        unique_imp_table, imp_table = [], []

        marg_NEs = get_NEs(marg_files)
        direct_NEs = get_NEs(dir_files)
        periph_NEs = get_NEs(periph_files)

        marg_imp = find_most_common(marg_NEs)
        main_imp = find_most_common(direct_NEs+periph_NEs)

        keywords = uf.remove_duplicates([x[0] for x in marg_imp] + [x[0] for x in main_imp])
        marg_keyword_apps = count_keyword_appearances(marg_NEs, keywords)
        main_keyword_apps = count_keyword_appearances(direct_NEs+periph_NEs, keywords)

        table = create_table(marg_keyword_apps, main_keyword_apps, keywords)
        calc_chi_square(table)