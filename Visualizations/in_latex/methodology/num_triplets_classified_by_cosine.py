import pandas as pd
import matplotlib.pyplot as plt
import universal_functions as uf

# GLOBAL
# Cosine 97
lowclass_cosine_folder = uf.get_files_from_folder(f"{uf.nep_location}BertClusteringClassification\\CosineClassification","pkl")
# Cosine 98
cosine_loc =f"{uf.nep_location}Reconstruction_Phase\\Cosine_Matching"
highclass_cosine_folder = uf.get_files_from_folder(cosine_loc,'pkl')
# Inner Layer
inner_layer = uf.get_files_from_folder(f"{uf.nep_location}Reconstruction_Phase\\Keyword_Matching","pkl")

# sort by partisanship
def get_data(cosine_folder):
    results = {}
    for file in cosine_folder:
        if 'separated' in file or 'emoji' in file or 'checkpoint' in file:
            continue
        cosine_data = uf.import_pkl_file(file)
        data_quantity = {}
        for k in ["Immigration", "Islamophobia","Anti-semitism","Transphobia"]:
            try:
                data_quantity[k]=len(cosine_data[k])
            except KeyError:
                data_quantity[k]=0

        dataset_name = uf.get_dataset_id(file)
        partisanship = dataset_name[:-7]
        if partisanship not in results.keys():
            results[partisanship] = {k:0 for k in data_quantity.keys()}

        il_loc = [x for x in inner_layer if f"\\{dataset_name}" in x]
        il_data = uf.import_pkl_file(il_loc[0])
        for k in data_quantity.keys():
            il_classified = [x for x in il_data['inner_layer'] if k in x['Category']]
            results[partisanship][k] += data_quantity[k] - len(il_classified)

    cols = ["Partisanship","Immigration", "Islamophobia","Anti-semitism","Transphobia"]
    plottable = []
    for p in results.keys():
        row = [p]
        for t in results[p].keys():
            row.append(results[p][t])
        plottable.append(row)

    df = pd.DataFrame(plottable, columns=cols)

    return df


def plot_num_triplets_classified_by_cosine(results, title):
    cols = ["Partisanship", "Immigration", "Islamophobia", "Anti-semitism", "Transphobia"]
    plottable = []
    for p in results.keys():
        row = [p]
        for t in results[p].keys():
            row.append(results[p][t])
        plottable.append(row)

    df = pd.DataFrame(plottable, columns=cols)
    # df = get_data(highclass_cosine_folder)

    # plotting graph
    fig = df.plot(x="Partisanship", y=["Immigration", "Islamophobia", "Anti-semitism", "Transphobia"], kind="bar")
    plt.tight_layout()
    plt.ylabel("Number of Triplets Classified through the Cosine Matching Process")
    plt.title(f"Number of Triplets Classified through the Cosine Matching Process by Partisanship, t={title}")
    plt.xticks(rotation=45)
    plt.show()
    # uf.export_as_pkl('Num_InnerLayer_Triplets.pkl',fig)

# get_data(cosine_folder=lowclass_cosine_folder)
# get_data(cosine_folder=highclass_cosine_folder)
# results_97 = {'CenterLeft': {'Immigration': 1983, 'Islamophobia': 992, 'Anti-semitism': 368, 'Transphobia': 20}, 'CenterRight': {'Immigration': 1075, 'Islamophobia': 515, 'Anti-semitism': 75, 'Transphobia': 12}, 'Center': {'Immigration': 1123, 'Islamophobia': 362, 'Anti-semitism': 224, 'Transphobia': 52}, 'FarLeft': {'Immigration': 3284, 'Islamophobia': 1450, 'Anti-semitism': 340, 'Transphobia': 77}, 'FarRight': {'Immigration': 2738, 'Islamophobia': 819, 'Anti-semitism': 488, 'Transphobia': 25}, 'Left': {'Immigration': 4838, 'Islamophobia': 1307, 'Anti-semitism': 311, 'Transphobia': 135}, 'Right': {'Immigration': 1024, 'Islamophobia': 429, 'Anti-semitism': 527, 'Transphobia': 10}}
results_97 = {'CenterLeft': {'Immigration': 1983, 'Islamophobia': 992, 'Anti-semitism': 368, 'Transphobia': 20}, 'CenterRight': {'Immigration': 1240, 'Islamophobia': 578, 'Anti-semitism': 95, 'Transphobia': 12}, 'Center': {'Immigration': 1485, 'Islamophobia': 450, 'Anti-semitism': 234, 'Transphobia': 52}, 'FarLeft': {'Immigration': 3284, 'Islamophobia': 1450, 'Anti-semitism': 340, 'Transphobia': 77}, 'FarRight': {'Immigration': 3801, 'Islamophobia': 987, 'Anti-semitism': 810, 'Transphobia': 73}, 'Left': {'Immigration': 4144, 'Islamophobia': 1686, 'Anti-semitism': 312, 'Transphobia': 194}, 'Right': {'Immigration': 1400, 'Islamophobia': 588, 'Anti-semitism': 664, 'Transphobia': 100}}
# results_98 = {'CenterLeft': {'Immigration': 367, 'Islamophobia': 188, 'Anti-semitism': 88, 'Transphobia': 3}, 'CenterRight': {'Immigration': 1, 'Islamophobia': 0, 'Anti-semitism': 0, 'Transphobia': 0}, 'Center': {'Immigration': 2, 'Islamophobia': 0, 'Anti-semitism': 0, 'Transphobia': 0}, 'FarLeft': {'Immigration': 284, 'Islamophobia': 0, 'Anti-semitism': 4, 'Transphobia': 19}, 'FarLeft_2-2017_pare': {'Immigration': 48, 'Islamophobia': 0, 'Anti-semitism': 0, 'Transphobia': 0}, 'FarRight': {'Immigration': 23, 'Islamophobia': 0, 'Anti-semitism': 0, 'Transphobia': 0}, 'Left': {'Immigration': 37, 'Islamophobia': 0, 'Anti-semitism': 0, 'Transphobia': 0}, 'Right': {'Immigration': 23, 'Islamophobia': 0, 'Anti-semitism': 0, 'Transphobia': 0}}
results_98 = {'CenterLeft': {'Immigration': 367, 'Islamophobia': 188, 'Anti-semitism': 88, 'Transphobia': 3}, 'CenterRight': {'Immigration': 2, 'Islamophobia': 0, 'Anti-semitism': 0, 'Transphobia': 0}, 'Center': {'Immigration': 3, 'Islamophobia': 0, 'Anti-semitism': 0, 'Transphobia': 0}, 'FarLeft': {'Immigration': 284, 'Islamophobia': 0, 'Anti-semitism': 4, 'Transphobia': 19}, 'FarRight': {'Immigration': 333, 'Islamophobia': 0, 'Anti-semitism': 18, 'Transphobia': 5}, 'Left': {'Immigration': 22, 'Islamophobia': 0, 'Anti-semitism': 0, 'Transphobia': 0}, 'Right': {'Immigration': 25, 'Islamophobia': 0, 'Anti-semitism': 0, 'Transphobia': 0}}
plot_num_triplets_classified_by_cosine(results_97,"0.97")
plot_num_triplets_classified_by_cosine(results_98,"0.985")
