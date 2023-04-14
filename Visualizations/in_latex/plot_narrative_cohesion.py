import matplotlib.pyplot as plt
import universal_functions as uf
import pandas as pd

summary_loc = f"{uf.thesis_location}Results\\Summarized_Narrative_Cohesion.csv"
summary = uf.import_csv(summary_loc)
cleaned_summary = [['Internal Cohesion', 'Marginal-Direct', 'Marginal-Peripheral', 'Direct-Peripheral']]
for row in summary[1:]:
    cleaned_summary.append([float(row[i]) for i in range(len(row)) if i !=0])

df = pd.DataFrame(cleaned_summary).T
df.columns = ["Metric",
              'Low Clustering, High Classification',
              'High Clustering, High Classification',
              "Low Clustering, Low Classification",
              "High Clustering, Low Classification"]
# df.index =['Internal Cohesion', 'Og to Direct', 'Og to Periph', 'Direct to Periph']

# plotting graph
fig = df.plot(x="Metric", y=['Low Clustering, High Classification',
              'High Clustering, High Classification',
              "Low Clustering, Low Classification",
              "High Clustering, Low Classification"], kind="bar")
plt.tight_layout()
plt.ylabel("Score")
plt.title("Average Cohesion Score By Pipeline and Metric")
plt.xticks(rotation=45)
plt.show()