import universal_functions as uf
from collections import Counter
import matplotlib.pyplot as plt

collection_conversion = {}

datasets = [x for x in uf.load_files_from_dataset(["text"])]
errors = []
for file in datasets:
    data = uf.import_csv(file)
    for row in data:
        if "ERROR:" in row[-1]:
            errors.append(row[-1])

counter = Counter(errors).most_common(10)
x, y = [],[]
for tup in counter:
    x.append(tup[0].replace("ERROR: ",""))
    y.append(tup[1])

fig = plt.bar(x,y)
plt.xticks(rotation=70)
plt.xlabel("Error Messages")
plt.ylabel("Quantity")
plt.tight_layout()
plt.show()
uf.export_as_pkl("Top10_error_msgs.fig.pkl",fig)