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
        num_newspapers[c_id] = [0,0]
    for row in data:
        if "ERROR:" in row[-1]:
            num_newspapers[c_id][0] += 1
    num_newspapers[c_id][1]+=len(data)

x, y1, y2 = [],[],[]
for k in num_newspapers.keys():
    x.append(k)
    y1.append(num_newspapers[k][0])
    y2.append(num_newspapers[k][1])

# plot bars in stack manner
plt.bar(x, y1, color='tab:blue')
plt.bar(x, y2, bottom=y1, color='tab:orange')
plt.legend(["Successfully Scraped", "Errors"])
plt.xticks(rotation=45)
plt.ylabel("Article Scrape Attempts")
plt.xlabel("Media Cloud Collections")
plt.tight_layout()
plt.show()