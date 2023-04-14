import universal_functions as uf
import matplotlib.pyplot as plt
import pandas as pd

manual_sim_eval_files = uf.get_files_from_folder(f"{uf.nep_location}Reconstruction_Phase\\Testing\\CosineMatching_Testing\\output","pkl")

x, y1, y2, y3 = [],[],[],[]
for file in manual_sim_eval_files:
    if "w_sent" in file:
        continue
    data = uf.import_pkl_file(file)
    threshold = file.split('Manual_sim_eval_')[1][:-4]
    x.append(threshold)
    correct, incorrect, unclear = 0,0,0
    for elt in data:
        # if elt['evaluation'] == '0':
        #     unclear+=1
        if elt['evaluation'] == '1':
            correct+=1
        if elt['evaluation'] == '-1':
            incorrect+=1
    y1.append(correct)
    # y2.append(unclear)
    y3.append(incorrect)


plt.bar(x, y1, color='tab:blue')
# plt.bar(x, y2, bottom=y1, color='tab:green')
plt.bar(x, y3, bottom=y1, color='tab:orange')
plt.legend(["Correct","Incorrect"])
plt.xticks(rotation=45)
plt.ylabel("Count")
plt.xlabel("Threshold")
plt.tight_layout()
plt.show()