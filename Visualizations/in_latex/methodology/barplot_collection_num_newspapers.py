import universal_functions as uf
import re
import matplotlib.pyplot as plt

collections = uf.load_files_from_dataset(["text"])

def get_collection_id(filename):
    regex = r"(?<=datasets\\)(.*?)(?=\_text)"
    dataset_name = re.findall(regex, filename)[0]

    conversion = {"CE19":"Center 2019",
                  "CL16":"Center Left 2016",
                  "CL19":"Center Left 2019",
                  "CO":"Conspiracies",
                  "CR16":"Center Right 2016",
                  "CR19":"Center Right 2019",
                  "FR":"Far Right",
                  "HL":"Hyperpartisan Left",
                  "HR":"Hyperpartisan Right",
                  "LL16":"Left 2016",
                  "LL19":"Left 2019",
                  "RR16":"Right 2016",
                  "RR19":"Right 2019",
                  }
    return conversion[dataset_name]

num_newspapers = {}
for c in collections:
    data = uf.import_csv(c)
    try:
        c_id = get_collection_id(c)
    except KeyError:
        continue
    if c_id not in num_newspapers.keys():
        num_newspapers[c_id] = []
    for row in data:
        if row[8] not in num_newspapers[c_id] and row[8]!='media_name':
            num_newspapers[c_id].append(row[8])

x,y=[],[]
for k in num_newspapers.keys():
    x.append(k)
    y.append(len(num_newspapers[k]))

plt.bar(x,y)
plt.xticks(rotation=45)
plt.xlabel('Media Cloud Collection')
plt.ylabel("Number of Newspapers ")
plt.tight_layout()
plt.show()