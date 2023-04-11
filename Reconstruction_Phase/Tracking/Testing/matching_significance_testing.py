import numpy as np
from scipy import stats
# chi-squared test with similar proportions
from scipy.stats import chi2_contingency
from scipy.stats import chi2
import universal_functions as uf


def chi_square_post_hoc(table, num_tests=6):
    stat, p, dof, expected = chi2_contingency(table)

    alpha = 0.05 / num_tests
    prob = 1 - alpha

    critical = chi2.ppf(prob, dof)
    print(f"Stat: {stat}")
    if abs(stat) >= critical:
        print('Dependent (reject H0)')
    else:
        print('Independent (fail to reject H0)')
    # interpret p-value

    # print('significance=%.3f, p=%.3f' % (alpha, p))
    if p <= alpha:
        print('Dependent (reject H0)')
    else:
        print('Independent (fail to reject H0)')

def unpack_matches(packed_matches):
    matches = {}
    for k in packed_matches:
        for t in packed_matches[k].keys():
            if t not in matches.keys():
                matches[t] = {}
            for elt in packed_matches[k][t]:
                if elt[0] not in matches[t].keys():
                    matches[t][elt[0]] = elt[1]
                else:
                    matches[t][elt[0]] += elt[1]
    return  matches

def calc_chi_square(table):
    stat, p, dof, expected = chi2_contingency(table)
    print('dof=%d' % dof)
    print(expected)
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



def create_table(matches):
    table = []
    for t in ["Immigration","Islamophobia","Anti-semitism","Transphobia"]:
        if t not in matches.keys():
            table.append([0, 0, 0, 0, 0, 0])
        else:
            row = []
            for p in ["Right", "CenterRight", "Center", "CenterLeft", "Left", "FarLeft"]:
                value = 0
                for k in matches[t].keys():
                    if p in k.split('_'):
                        value += matches[t][k]
                row.append(value)

            table.append(row)
    return  table

def post_hoc(table):
    labels = ["Immigration","Islamophobia","Anti-semitism","Transphobia"]
    for i in range(len(table)):
        for j in range(len(table)):
            if i!=j:
                print(f"\n\n{labels[i]} {i}, {labels[j]}, {j}")
                new_table = [table[i],table[j]]
                chi_square_post_hoc(new_table)


# for k in matches_97.keys():
#     table = []
#     for t in ["Immigration","Islamophobia","Anti-semitism","Transphobia"]:
#         if t not in matches_97[k].keys():
#             table.append([0, 0,  0, 0, 0, 0])
#         else:
#             row = []
#             for p in ["Right","CenterRight","Center","CenterLeft","Left","FarLeft"]:
#                 p_value = [x[1] for x in matches_97[k][t] if p in x[0].split("_")]
#                 if len(p_value) < 1:
#                     row.append(0)
#                 else:
#                     row.append(p_value[0])
#             table.append(row)
#     try:
#         calc_chi_square(table)
#     except ValueError:
#         continue

matches_97 = uf.import_json_content("97_common_matches.json")
matches_97_20_packed = {k:matches_97[k] for k in matches_97.keys() if "0.2" in k}
matches_97_20 = unpack_matches(matches_97_20_packed)
table = create_table(matches_97_20)
calc_chi_square(table)
post_hoc(table)