import universal_functions as uf
import pandas as pd
import matplotlib.pyplot as plt


def condense_results_by_year(results):
    condensed = {}
    for k in results.keys():
        part = k[:-7]
        if part not in condensed.keys():
            condensed[part] = {}
        for t in results[k].keys():
            if t not in condensed[part].keys():
                condensed[part][t]= results[k][t]
            else:
                condensed[part][t]+=results[k][t]
    return condensed

keyword_matches = uf.get_files_from_folder(f"{uf.nep_location}Reconstruction_Phase\\Keyword_Matching","pkl")
sentiment = ["separated","emoji","colon","parentheses"]


# #
# result = {}
# for file in keyword_matches:
#     dv = False
#     for s in sentiment:
#         if s in file:
#             dv = True
#     if dv == True:
#         continue
#     dataset_name = uf.get_dataset_id(file)
#     result[dataset_name] ={}
#     data = uf.import_pkl_file(file)
#     for elt in data['inner_layer']:
#         for cat in elt['Category']:
#             if cat not in result[dataset_name].keys():
#                 result[dataset_name][cat] = 1
#             else:
#                 result[dataset_name][cat] += 1
# uf.content_json_export("Num_Inner_Layer_classifications.json",result)
uncondensed_result = uf.import_json_content("../Num_Inner_Layer_classifications.json")
result = condense_results_by_year(uncondensed_result)

plottable = {"Dataset":[],
             "Immigration":[],
             "Islamophobia":[],
             "Anti-semitism":[],
             "Transphobia":[]
             }
for k in result.keys():
    plottable['Dataset'].append(k)
    for t in plottable.keys():
        if t == "Dataset":
            continue
        if t not in result[k].keys():
            plottable[t].append(0)
        else:
            plottable[t].append(result[k][t])


df = pd.DataFrame(plottable)

# plotting graph
fig = df.plot(x="Dataset", y=["Immigration", "Islamophobia","Anti-semitism","Transphobia"], kind="bar")
plt.tight_layout()
plt.ylabel("Number of Classified Triplets")
plt.xticks(rotation=45)
plt.show()
uf.export_as_pkl('Num_InnerLayer_Triplets.pkl',fig)