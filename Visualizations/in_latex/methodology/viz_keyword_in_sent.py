import universal_functions as uf
import matplotlib.pyplot as plt

import pandas as pd

def plot_grouped_barplot(df, x, rotation):
    # plotting graph
    fig = df.plot(x=x, y=["t=0.97", "t=0.985"], kind="bar")
    plt.tight_layout()
    plt.ylabel("Percent")
    plt.xticks(rotation=rotation)
    plt.show()


# Topic 0.97 0.985 Barplot y axis score
def plot_by_topic(data):
    results = {"t=0.97":{}, "t=0.985":{}}
    for row in data:
        if row[0]=="97":
            if row[2] not in results["t=0.97"].keys():
                results["t=0.97"][row[2]]=[]
            results["t=0.97"][row[2]].append(float(row[-1]))
        elif row[0]=="98":
            if row[2] not in results["t=0.985"].keys():
                results["t=0.985"][row[2]]=[]
            results["t=0.985"][row[2]].append(float(row[-1]))

    col = ['Topic',"t=0.97","t=0.985" ]
    frameable = [[k, None, None] for k in results["t=0.985"].keys()]
    for c in results.keys():
        if c == "t=0.97":
            for t in results[c].keys():
                results[c][t] = sum(results[c][t] )/len(results[c][t] )
                for r in frameable:
                    if r[0]==t:
                        r[1]=results[c][t]
        if c == "t=0.985":
            for t in results[c].keys():
                results[c][t] = sum(results[c][t]) / len(results[c][t])
                for r in frameable:
                    if r[0] == t:
                        r[2] = results[c][t]
    df = pd.DataFrame(frameable, columns=col)
    plot_grouped_barplot(df, "Topic",0)

def plot_by_dataset(data):
    results = {"t=0.97": {}, "t=0.985": {}}
    for row in data:
        dataset = uf.get_dataset_id(row[1])

        if row[0] == "97":
            if dataset not in results["t=0.97"].keys():
                results["t=0.97"][dataset] = []
            results["t=0.97"][dataset].append(float(row[-1]))
        elif row[0] == "98":
            if dataset not in results["t=0.985"].keys():
                results["t=0.985"][dataset] = []
            results["t=0.985"][dataset].append(float(row[-1]))

    col = ['Year', "t=0.97", "t=0.985"]
    frameable = [[k, None, None] for k in list(results["t=0.985"].keys())+list(results["t=0.97"].keys())]
    for c in results.keys():
        if c == "t=0.97":
            for t in results[c].keys():
                results[c][t] = sum(results[c][t]) / len(results[c][t])
                for r in frameable:
                    if r[0] == t:
                        r[1] = results[c][t]
        if c == "t=0.985":
            for t in results[c].keys():
                results[c][t] = sum(results[c][t]) / len(results[c][t])
                for r in frameable:
                    if r[0] == t:
                        r[2] = results[c][t]
    df = pd.DataFrame(frameable, columns=col)
    df=df.dropna()
    plot_grouped_barplot(df, "Year",45)

def plot_by_num_elts(data):
    x,y = [],[]
    for row in data:
        x.append(int(row[3]))
        y.append(float(row[4]))
    plt.scatter(x,y)
    plt.xlabel('Number of Triplets in the Dataset')
    plt.ylabel("% Keywords in Source Sentence")
    plt.show()


data = uf.import_csv('../../../stats_collection_for_writings/cosine_matching_evaluations/Keyword_in_sent_eval.csv')
# By topic
plot_by_topic(data)

# Dataset 0.97 0.985 Barplot y axis score
plot_by_dataset(data)

# X axis num elts in dataset y axis score
plot_by_num_elts(data)
