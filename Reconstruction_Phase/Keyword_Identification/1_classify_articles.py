"""
First step
Classify articles
"""

import universal_functions as uf
import json
import random
from typing import List


def get_prev_keywords(classification:List[dict])->List[str]:
    # Fetch all words previously identified as potential keywords
    prev_keywords = []
    for obj in classification:
        if obj['labels']=='Other':
            continue
        for key in obj['labels'].keys():
            if key =='Immigration': # TODO: Ignores all found immigration keywords
                continue
            try:
                keywords = obj['labels'][key]['keywords'].split(';')

            except AttributeError:
                keywords = obj['labels'][key]['keywords']
            for word in keywords:
                if word not in prev_keywords:
                    prev_keywords.append(word)
    return prev_keywords


def find_matching_row(datasets:List[str],keywords:List[str]):
    # match = []
    while True: # Endless loop
        loc = random.choice(datasets) # Chose a random file
        data = uf.import_csv(loc) # Import the file
        row = random.choice(data) # Choose a random row

        for w in keywords: # Iterate through all the keywords
            if f" {w} " in row[-1].lower(): # if the word appears in the article text
                print(f'Found word: {w}') # print the word
                return loc,row # return the filename and the matched row



def classify_new_articles(with_hints:bool):
    conversion = {"1": 'Immigration', "2": 'Islamophobia', "3": 'Anti-semitism', "4": 'Transphobia',"5":"Other"}
    classified = uf.import_json_content("Keyword_Article_Classification.json")
    print(f'{len(classified)} article have been classified so far\n\n')
    if with_hints==True:
        existing_keywords = get_prev_keywords(classified)

    while True:
        prepped_datasets = uf.load_all_complete_datasets()

        if with_hints==True:
            dataset_loc, row = find_matching_row(prepped_datasets,existing_keywords)
        else:
            dataset_loc = random.choice(prepped_datasets)
            dataset = uf.import_csv(dataset_loc)
            row = random.choice(dataset)

        print(f"\nArticle text: {row[-1]}")
        labels = input('Immigration:1,Islamophobia:2,Anti-semitism:3,Transphobia:4,Other:5')
        if labels=='quit':
            a_content = json.dumps({'content': classified})
            uf.export_as_json("Keyword_Article_Classification.json", a_content)
            return
        labels = [conversion[x] for x in labels.split(',')]
        obj = {"dataset": dataset_loc, "article_id": row[0]}
        if 'Other' in labels:
            obj['labels'] = 'Other'
            classified.append(obj)
        else:
            justifications = input('New justifications:')
            keywords = input("New keywords:")

            obj['labels'] = {}
            for i in range(len(labels)):
                obj['labels'][labels[i]]={'justifications':justifications.split(',')[i],'keywords':keywords.split(",")[i]}
            classified.append(obj)


## ACTION ##
if __name__ == '__main__':
    classify_new_articles(with_hints=True)
