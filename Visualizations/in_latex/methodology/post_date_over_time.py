import universal_functions as uf
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


def count_datetimes(data):
    dates ={}
    for row in data:
        if row[1] !='publish_date' and row[1]!="":
            if len(row[1])>19:
                row[1]=row[1][:19]
            date = datetime.strptime(row[1][5:][:-6],'%m-%d %H')
            if date in dates.keys():
                dates[date]+=1
            else:
                dates[date]=1

    x = list(dates.keys())
    y = list(dates.values())
    df = pd.DataFrame(data=[x,y]).T
    df.columns=['Date','Frequency']
    df = df.sort_values(by='Date')
    return list(df.Date), list(df.Frequency)


def plot_date_frequency(x,y):
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    fig = plt.plot(x,y)
    plt.gcf().autofmt_xdate()
    plt.xlabel('Date (dd/mm)')
    plt.ylabel('Number of articles published')
    plt.title('Publication times for all articles')
    plt.show()
    uf.export_as_pkl('Publication_times_for_all_articles.fig.pkl',fig)


def plot_many_date_frequencies(X,Y):
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    for i in range(len(X)):
        plt.plot(X[i], Y[i])
    plt.gcf().autofmt_xdate()
    plt.xlabel('Date')
    plt.ylabel('Number of article published')
    plt.title('Publication Times for all Datasets')
    plt.show()

def combine_dates(files):
    dates = {}
    for file in files:
        data = uf.import_csv(file)

        for row in data:
            if row[1] != 'publish_date' and row[1] != "":
                if len(row[1]) > 19:
                    row[1] = row[1][:19]
                date = datetime.strptime(row[1][5:][:-6], '%m-%d %H')
                if date in dates.keys():
                    dates[date] += 1
                else:
                    dates[date] = 1

    x = list(dates.keys())
    y = list(dates.values())
    df = pd.DataFrame(data=[x, y]).T
    df.columns = ['Date', 'Frequency']
    df = df.sort_values(by='Date')
    return list(df.Date), list(df.Frequency)


complete_datasets = uf.load_all_complete_datasets()

# GET JUST ONE FILE'S PLOT
# file = complete_datasets[0]
# data = uf.import_csv(file)
# x,y=count_datetimes(data)
# plot_date_frequency(x,y)

# PLOT ALL THE DATASETS ON ONE GRAPH
# X,Y=[],[]
# for file in complete_datasets:
#     data = uf.import_csv(file)
#     x,y=count_datetimes(data)
#     X.append(x)
#     Y.append(y)
#
# plot_many_date_frequencies(X,Y)

# # PLOT GRAND TOTAL
x,y=combine_dates(complete_datasets)
plot_date_frequency(x,y)