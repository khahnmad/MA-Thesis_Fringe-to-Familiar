# plot overlap over tiem
"""COMPLETE"""
import matplotlib.pyplot as plt
import universal_functions as uf

cosine_97 = f"{uf.thesis_location}Results\\rq_2\\no_sent\\cosine_97\\"
cosine_98 = f"{uf.thesis_location}Results\\rq_2\\no_sent\\cosine_98\\"

def plot_percent_overlap_by_year():
    labels = ["Low Clustering, Low Classification","High Clustering, Low Classification",
              'Low Clustering, High Classification','High Clustering, High Classification']
    files = [f"{cosine_97}20_overlap_by_year.csv",f"{cosine_97}30_overlap_by_year.csv",
              f"{cosine_98}20_overlap_by_year.csv",f"{cosine_98}30_overlap_by_year.csv"]
    for i in range(len(files)):
        data = uf.import_csv(files[i])
        x = [x[0][-4:] for x in data]
        y = [float(y[1]) for y in data]
        plt.plot(x,y,label=labels[i])
    plt.legend()
    plt.xlabel('Year')
    plt.ylabel('Percent Overlap')
    plt.title('Percent Overlap in Named Entities between Marginal and Mainstreamed Narrative Instances')
    plt.show()

def plot_percent_overlap_by_topic():
    labels = ["Low Clustering, Low Classification", "High Clustering, Low Classification",
              'Low Clustering, High Classification', 'High Clustering, High Classification']
    files = [f"{cosine_97}20_overlap_by_topic.csv", f"{cosine_97}30_overlap_by_topic.csv",
             f"{cosine_98}20_overlap_by_topic.csv", f"{cosine_98}30_overlap_by_topic.csv"]
    for i in range(len(files)):
        data = uf.import_csv(files[i])
        x = [x[0] for x in data]
        y = [float(y[1]) for y in data]
        plt.scatter(x, y, label=labels[i])
    plt.legend()
    plt.xlabel('Topic')
    plt.ylabel('Percent Overlap')
    plt.title('Percent Overlap in Named Entities between Marginal and Mainstreamed Narrative Instances')
    plt.show()

plot_percent_overlap_by_year()
plot_percent_overlap_by_topic()