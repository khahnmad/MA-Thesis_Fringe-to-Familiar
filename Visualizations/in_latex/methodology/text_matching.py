import universal_functions as uf
import matplotlib.pyplot as plt

manual_sim_eval_files = uf.get_files_from_folder(f"{uf.nep_location}Reconstruction_Phase\\Testing\\CosineMatching_Testing\\output","pkl")

results = {}
for file in manual_sim_eval_files:
    if "w_sent" in file:
        continue
    data = uf.import_pkl_file(file)
    threshold = file.split('Manual_sim_eval_')[1][:-4]
    results[threshold]=[]

    for elt in data:
        count = 0
        matched_sentence = elt['threshold_match'][3]
        if f"{elt['subject']} " in matched_sentence:
            count += 1
        if f" {elt['relation']} " in matched_sentence:
            count  +=1
        if f" {elt['object']}" in matched_sentence:
            count+=1
        results[threshold].append(count)
x,y =[],[]
for k in results.keys():
    x.append(k)
    y.append( (sum(results[k])/len(results[k]))/3)

plt.bar(x, y)
plt.xlabel('Cosine Similarity Threshold')
plt.ylabel("Percent shared text between matches")
plt.show()
print('check')
