import ast
import csv
import sys
import glob
from sklearn.cluster import KMeans
import sklearn
from typing import List
import pandas as pd
from plotly import express as px
from sklearn.manifold import TSNE
import re
import json
import matplotlib.pyplot as plt
import pickle
import numpy as np
from pathlib import Path
from os.path import dirname

### VARIABLES ###
# nep_location = 'C:\\Users\\khahn\\Documents\\Github\\Thesis\\NarrativeExtractionPipeline\\'
# thesis_location = 'C:\\Users\\khahn\\Documents\\Github\\Thesis\\'
repo_loc = Path(dirname(__file__))


### IMPORTING ###
def manage_overflow():
    # Manages overflow from importing .csv files with lots of text data in one column
    maxInt = sys.maxsize
    while True:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.
        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)


def get_files_from_folder(folder_name:str, file_endings:str)->List[str]:
    return [x for x in glob.glob(folder_name + f"/*.{file_endings}")]


def import_pkl_file(file):
    with open(file, "rb") as f:
        pkl_file = pickle.load(f)
        f.close()
    return pkl_file


def import_json_content(file:str):
    with open(file, 'r') as j:
        content = json.loads(j.read())['content']
    return content


def import_csv(csv_file:str)->List[List]:
    # Given a file location, imports the data as a nested list, each row is a new list
    manage_overflow() # manage overflow from large lines
    nested_list = []  # initialize list
    with open(csv_file, newline='', encoding='utf-8') as csvfile:  # open csv file
        reader = csv.reader(csvfile, delimiter=',')
        try:
            for row in reader:
                nested_list.append(row)  # add each row of the csv file to a list
        except Exception as e:
            # NOTE: can't reproduce the error that I created this code for... not sure how to improve
            df = pd.read_csv(csv_file)
            columns = [list(df.columns)]
            nested_list = columns + df.values.tolist()
            for i in range(len(nested_list)):
                new_row = [str(x) for x in nested_list[i]]
                nested_list[i] = new_row
            print(f"CAUTION: {e} for file {csv_file}\n")
    return nested_list


def load_files(req_strings: list, dataset_files:List[str]) -> List[str]:
    relevant_files = []
    for file in dataset_files:  # iterate through the existing dataset files
        count = 0
        for req in req_strings:  # iterate through the query strings
            if req in file:
                count += 1
        if count == len(req_strings):  # make sure that all the req strings were counted in the file
            relevant_files.append(file)
    return relevant_files # debug: check that this still works even though I've moved the functions around


def load_files_from_dataset(req_strings: list) -> list:
    # Given query strings (req_strings), returns a list of file locations from the dataset that match
    all_dataset_files = [x for x in glob.glob(str(repo_loc / "Data_Collection/Media_Cloud") + "/*.csv")]
    relevant_files = load_files(req_strings, all_dataset_files)
    return relevant_files


def load_files_from_prepped_datasets(req_strings:list)-> list:
    # Given query strings (req_strings), returns a list of file locations from the prepped dataset that match
    all_dataset_files = [x for x in glob.glob(str(repo_loc / 'Data_Collection/Final_Processing/Datasets') + "/*.csv")]
    relevant_files = load_files(req_strings, all_dataset_files)
    return relevant_files


def get_dataset_year(filename:str)->str:
    regex = r"(?<=prepped_dataset\\)(.*?)(?=\_)"
    dataset_name = re.findall(regex, filename)[0]
    return dataset_name


def get_dataset_id(filename:str)->str:
    # Reconstruction Phase
    if 'Keyword_Matching' in filename or "Cosine_Matching" in filename:
        regex = r"(?<=Matching\\)(.*?)(?=\_Emb)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if 'Kmeans_Output' in filename:
        regex = r"(?<=Output\\)(.*?)(?=\_Emb)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name

    # Tracking
    if "Threshold\\Marginal" in filename:
        regex = r"(?<=Narratives\\)(.*?)(?=\_0)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if 'Threshold' in filename:
        regex = r"(?<=Threshold\\)(.*?)(?=\_0)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if 'Tracking' in filename:
        regex = r"(?<=Narratives\\)(.*?)(?=\_0)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name

    # Results
    if 'unique_narratives' in filename:
        regex = r"(?<=narratives\\)(.*?)(?=\_unique)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if "first_step" in filename:
        regex = r"(?<=step\\)(.*?)(?=\_first)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if "second_step" in filename:
        regex = r"(?<=step\\)(.*?)(?=\_second)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name


    # Earlier
    if 'Sentiment' in filename and "Reduced_SROs" in filename:
        regex = r"(?<=Reduced_SROs\\)(.*?)(?=\_R)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if 'Sentiment' in filename:
        regex = r"(?<=Sentiment_Instances\\)(.*?)(?=\_Sentiment)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if 'SRO_Instances' in filename:
        regex = r"(?<=SRO_Instances\\)(.*?)(?=\_SRO)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if 'AggregatedConcepts' in filename:
        regex = r"(?<=AggregatedConcepts\\)(.*?)(?=\_AggregatedConcepts)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if 'Filtered_Keywords' in filename:
        regex = r"(?<=Filtered_Keywords\\)(.*?)(?=\_ClassifiedClusters)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if 'Original_keywords' in filename:
        regex = r"(?<=keywords\\)(.*?)(?=\_ClassifiedClusters)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if '\\Embeddings' in filename:
        regex = r"(?<=\\Embeddings\\)(.*?)(?=\_embeddings)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if 'Reduced_SROs' in filename:
        regex = r"(?<=Reduced_SROs\\)(.*?)(?=\_Reduced)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if 'InnerLayer' in filename and 'Sent' not in filename:
        regex = r"(?<=InnerLayer\\)(.*?)(?=\_Emb)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if 'uncase_earlier' in filename:
        regex = r"(?<=keywords\\)(.*?)(?=\_Emb)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if 'CosineClassification' in filename and "Sent_" not in filename:
        regex = r"(?<=CosineClassification\\)(.*?)(?=\_Emb)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if 'KmeansOutput' in filename and 'Diff_percent' not in filename:
        regex = r"(?<=KmeansOutput\\)(.*?)(?=\_Emb)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if 'unique_narratives' in filename and 'Unique' in filename:
        regex = r"(?<=Narratives\\)(.*?)(?=\_unique)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if 'unique_narratives' in filename and '30_perc' in filename:
        regex = r"(?<=percent\\)(.*?)(?=\_unique)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if 'Related_Narratives' in filename:
        regex = r"(?<=\\Tracking\\)(.*?)(?=\_Related)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if 'FirstOrder' in filename:
        regex = r"(?<=\\Tracking\\)(.*?)(?=\_FirstOrder)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if "FirstStep" in filename:
        regex = r"(?<=Narratives\\)(.*?)(?=\_first_step)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if "SecondStep" in filename:
        regex = r"(?<=Narratives\\)(.*?)(?=\_second)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if '\\datasets' in filename:
        r1 = r"(?<=datasets\\)(.*?)(?=\_text)"
        name = re.findall(r1, filename)[0]
        r2 = r"(?<=text\_)(.*?)(?=\_|\.)"
        year = re.findall(r2, filename)[0]
        dataset_name = f"{name}_{year}"
        return dataset_name
    if "Diff_percent" in filename:
        regex = r"(?<=Diff_percent\\)(.*?)(?=\_Emb)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if '30_percent' in filename and 'first' in filename:
        regex = r"(?<=30_percent\\)(.*?)(?=\_first)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if '30_percent' in filename and 'second' in filename:
        regex = r"(?<=30_percent\\)(.*?)(?=\_second)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if "CosineClassification\\Sent_Emb" in filename:
        regex = r"(?<=Embeddings\\)(.*?)(?=\_Emb)"
        dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    if 'Sent_Embeddings' in filename:
        try:
            regex = r"(?<=\_Embeddings\\)(.*?)(?=\_emb)"
            dataset_name = re.findall(regex, filename)[0]
        except IndexError:
            regex = r"(?<=\_Embeddings\\)(.*?)(?=\_Keyword)"
            dataset_name = re.findall(regex, filename)[0]
        return dataset_name
    regex = r"(?<=prepped_dataset\\)(.*?)(?=\.csv)"
    dataset_name = re.findall(regex, filename)[0]
    return dataset_name


def load_all_complete_datasets()->List[str]:
    all_prepped_files = load_files_from_prepped_datasets([])
    complete_datasets = []

    acceptable={'FarLeft':['2016_INCOMPLETE','2017_INCOMPLETE','2018_INCOMPLETE','2019_INCOMPLETE','2020_INCOMPLETE','2021.csv'],
                'Left':['2016.csv','2017.csv','2018.csv','2019.csv','2020.csv','2021.csv'],
                'CenterLeft':['2016.csv','2017.csv','2018.csv','2019.csv','2020.csv','2021.csv'],
                'Center':['2016.csv','2017.csv','2018.csv','2019.csv','2020.csv'],
                'CenterRight':['2016.csv','2017.csv','2018.csv','2019.csv','2020.csv','2021.csv'],
                'FarRight':['2016.csv','2017.csv','2018.csv','2019.csv','2020.csv','2021.csv'],
                'Right':['2016.csv','2017.csv','2018.csv','2019.csv','2020.csv','2021.csv']}

    for file in all_prepped_files:
        dataset_name = get_dataset_id(file)[:-7]
        if dataset_name.endswith('_INC'):
            dataset_name=dataset_name[:-11]
        if dataset_name in acceptable.keys():
            for v in acceptable[dataset_name]:
                if v in file:
                    complete_datasets.append(file)
    return complete_datasets


def load_manual_eval_as_dict()->dict:
    """
    Loads the scraping manual evaluation .csv file as a dictionary where:
    key: filename
    value: [correctly labeled scrape, incorrectly labeled scrape], [correctly labeled error, incorrectly labelled error]
    """
    manual_file_name = 'C:\\Users\\khahn\\Documents\\Github\\Thesis\\scraping_evals\\associated_python\\Manual_evaluation.csv'
    list_format = import_csv(manual_file_name) # import the file as a list

    two_item = [True for row in list_format if len(row)==2] # Check that are two lists
    if all(two_item) is False:
        raise Exception('There are not two items in each row')

    two_sublists = [True for row in list_format if len(ast.literal_eval(row[1])) == 2]  # Check there are two sublists
    if all(two_sublists) is False:
        raise Exception('There are not two sublists in each row')

    k = [x[0] for x in list_format]
    v = [ast.literal_eval(x[1]) for x in list_format]  # correct str importation
    dict_format = dict(zip(k, v))
    return dict_format


### PREPROCESSING ###
def clean_concept(concept:List[str])->List[List[str]]:
    # Takes the messed up format from the .csv file and turns it into the expected format
    replaceable = ["[", "]", "'"]
    cleaned = []
    for subcomponent in concept:
        for elt in replaceable:
            subcomponent=subcomponent.replace(elt,"")
        partially_cleaned_sub = subcomponent.split(",")
        cleaned_sub = []
        for item in partially_cleaned_sub:
            if item.startswith('  '):
                item = item[2:]
            if item.startswith(' '):
                item = item[1:]
            if item.endswith('  '):
                item = item[:-2]
            cleaned_sub.append(item)
        cleaned.append(cleaned_sub)
    return cleaned


def make_lowercase(list_strings:list)->list:
    return [x.lower() for x in list_strings]


### EXPORTING ###
def export_list(csv_name:str, data_item:list):
    # Export a single list as a csv with one row
    with open(csv_name, 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(data_item)


def export_nested_list(csv_name:str, nested_list:List[List]):
    # Export a nested list as a csv with a row for each sublist
    with open(csv_name, 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in nested_list:
            writer.writerow(row)


def export_manual_sample(manual_sample_as_dict:dict):
    # Export the dictionary form of the scraping manual sampling as a csv with a row for each item in the dictionary
    manual_file_name = '/scraping_evals/associated_python/Manual_evaluation.csv'
    exportable_record = [list(row) for row in manual_sample_as_dict.items()]
    export_nested_list(manual_file_name, exportable_record)


def export_as_json(export_filename:str, output):
    if export_filename.endswith('.json') is not True:
        raise Exception(f"{export_filename} should be a .json file")
    with open(export_filename, "w") as outfile:
        outfile.write(output)

def content_json_export(export_name, data):
    content = json.dumps({'content': data})
    export_as_json(export_name, content)

def export_as_pkl(export_name:str, content):
    with open(export_name, "wb") as f:
        pickle.dump(content, f)
        f.close()


### MISCELLANEOUS ###
def tsne_visualization(texts: List[str], labels: List[str], embeddings: List, title):
    arr = np.array(embeddings)
    X_embedded = TSNE(n_components=2).fit_transform(arr)
    df_embeddings = pd.DataFrame(X_embedded)
    df_embeddings = df_embeddings.rename(columns={0: 'x', 1: 'y'})
    df_embeddings = df_embeddings.assign(label=labels)
    df_embeddings = df_embeddings.assign(text=texts)

    fig = px.scatter(
        df_embeddings,
        x='x',
        y='y',
        color='label',
        labels={'color': 'label'},
        hover_data=['text'],
        title=title
    )
    fig.show()

def plot_3d(x_label:str, y_label:str, z_label:str, X:List[float],Y:List[float],Z:List[float],text:List[str],title:str,save:bool):

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_zlabel(z_label)

    for i in range(len(text)):
        ax.text(X[i], Y[i],Z[i], text[i])

    ax.scatter(X, Y, Z)
    plt.show()
    if save == True:
        pickle.dump(fig, open(f'{title}.fig.pickle', 'wb'))


def remove_duplicates(data:list)->list:
    new_list  =[]
    for elt in data:
        if elt not in new_list:
            new_list.append(elt)
    return new_list


def evaluate_kmeans(data,max_num_clusters):
    best_score = [0,0]

    for i in range(2,max_num_clusters):
        kmeans = KMeans(n_clusters=i, random_state=0).fit(data)
        silhouette_score = sklearn.metrics.silhouette_score(X=data, labels = kmeans.labels_) # NOTE: sometimes get an error that im calling a nonetype when debugging
        if silhouette_score > best_score[1]:
            best_score = [i, silhouette_score]
            # print(f"Num clusters:{i}\nSilhouette score:{silhouette_score}\n")

    return best_score

def flatten_list(data):
    flattened = []
    for li in data:

        flattened+=li
    return flattened

