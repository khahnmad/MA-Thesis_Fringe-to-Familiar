from collections import Counter
import matplotlib.pyplot as plt
import universal_functions as uf


def plot_top_newspapers_by_year(fs_pushers, title):
    data = uf.import_csv(fs_pushers)
    top = []
    for row in data:
        top += [row[2]] * int(row[3])
    papers = [x[0] for x in Counter(top).most_common(5)]
    results = {k:{"2016":0,"2017":0,"2018":0,"2019":0} for k in papers}
    for row in data:
        if row[2] in papers:
            year = row[0][-4:]
            freq = int(row[-1])
            results[row[2]][year] = freq
    for p in results.keys():
        x = results[p].keys()
        y = results[p].values()
        plt.plot(x,y,label=p)
    plt.xlabel("Year")
    plt.legend()
    plt.ylabel("Number of Mainstreamed Narratives Contributed To")
    plt.title(title)
    plt.show()



pusher_97_20 = f"{uf.thesis_location}Results\\pushers\\no_sent\\cosine_97\\20_fs_pushers.csv"
pusher_97_30 = f"{uf.thesis_location}Results\\pushers\\no_sent\\cosine_97\\30_fs_pushers.csv"
pusher_98_20 = f"{uf.thesis_location}Results\\pushers\\no_sent\\cosine_98\\20_fs_pushers.csv"
pusher_98_30 = f"{uf.thesis_location}Results\\pushers\\no_sent\\cosine_98\\30_fs_pushers.csv"

labels = ['Low Clustering, Low Classification',
          "High Clustering, Low Classification",
          'Low Clustering, High Classification',
          'High Clustering, High Classification']

pushers = [pusher_97_20, pusher_97_30, pusher_98_20, pusher_98_30]

for i in range(len(pushers)):
    plot_top_newspapers_by_year(pushers[i],labels[i])