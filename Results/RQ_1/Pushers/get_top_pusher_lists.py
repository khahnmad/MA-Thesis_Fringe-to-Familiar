import universal_functions as uf
from Results.locations import *
from collections import Counter

marginal_narratives = uf.import_csv(f"{uf.thesis_location}Results\\hypothesis_a\\Num_Marginal_Narratives.csv")

def convert_to_dict(nested_list):
    dict_form = {}
    for row in nested_list:
        if row[0] not in dict_form.keys():
            dict_form[row[0]] = {}
        if row[1] not in dict_form[row[0]].keys():
            dict_form[row[0]][row[1]] = []
        dict_form[row[0]][row[1]].append([row[2],float(row[3])])
    return dict_form

def get_relative_to_marginal_top_pushers(title, marg_row):
    file = f"{title}_fs_pushers.csv"
    pusher_list = uf.import_csv(file)
    pusher_dict = convert_to_dict(pusher_list)

    exportable = []
    for ds in pusher_dict.keys():
        for t in pusher_dict[ds].keys():
            given_marginal = [x for x in marginal_narratives if x[1]==ds and x[2]==t][0]
            for row in pusher_dict[ds][t]:
                percent = row[1]/float(given_marginal[marg_row])
                exportable.append([ds, t, row[0], percent])
    uf.export_nested_list(f"{title}_rel_marg_pushers.csv",exportable)

def get_num_articles(newspaper, dataset, topic, title):

    news_art_ids = uf.import_json_content(f"{title}_newspaper_appearances.json")
    result = news_art_ids[dataset][topic][newspaper]
    return int(result)


def match_newspapers(kmeans_folder, title):
    # Get article ids
    article_ids = {}
    for file in kmeans_folder:
        data = uf.import_pkl_file(file)
        datset_name = uf.get_dataset_id(file)

        article_ids[datset_name] = {}
        for t in data.keys():
            article_ids[datset_name][t] = []
            for elt in data[t]['narratives_classified']:
                if elt['article_id'] not in article_ids[datset_name][t]:
                    article_ids[datset_name][t].append(elt['article_id'])

    newspaper_article_id_matches = {}
    for ds in article_ids.keys():
        if '0.2' in ds or '0.3' in ds:
            dataset_name = ds[:-4]
        else:
            dataset_name = ds
        text_loc = [x for x in uf.load_all_complete_datasets() if f"\\{dataset_name}" in x]
        if len(text_loc)>1:
            print('cjeck')
            continue
        if len(text_loc)<1:
            print('check')
            continue
        text_data = uf.import_csv(text_loc[0])

        for t in article_ids[ds].keys():
            for a_id in article_ids[ds][t]:
                try:
                    newspaper = [x[8] for x in text_data if x[0] == a_id][0]
                except IndexError:
                    newspaper = "NOT FOUND"
                if newspaper not in newspaper_article_id_matches.keys():
                    newspaper_article_id_matches[newspaper] = []
                newspaper_article_id_matches[newspaper].append(a_id)
    uf.content_json_export(f'{title}_newspaper_article_id_matches.json',newspaper_article_id_matches)


def get_num_newspaper_appearances(kmeans_folder, title):
    result = {}
    for file in kmeans_folder:
        data = uf.import_pkl_file(file)
        dataset_name = uf.get_dataset_id(file)
        if '0.2' in dataset_name or '0.3' in dataset_name:
            dataset_name = dataset_name[:-4]
            # print('check')

        text_loc = [x for x in uf.load_all_complete_datasets() if f"\\{dataset_name}" in x]
        if len(text_loc) > 1:
            print('cjeck')
            continue
        if len(text_loc) < 1:
            print('check')
            continue
        text_data = uf.import_csv(text_loc[0])

        result[dataset_name] ={}
        for t in data.keys():
            result[dataset_name][t]={}
            # Get the article ids from the kmeans clustering analysis
            art_ids = uf.remove_duplicates([x['article_id'] for x in data[t]['narratives_classified']])
            newspapers = []
            for a_id in art_ids:
                # Get newspaper
                try:
                    newspaper = [x[8] for x in text_data if x[0]==a_id][0]
                except IndexError:
                    continue
                newspapers.append(newspaper)
            counter = Counter(newspapers)
            for c in counter.keys():
                result[dataset_name][t][c] = counter[c]
    uf.content_json_export(f'{title}_newspaper_appearances.json', result)

def get_relative_to_articles_top_pushers(title):
    file = f"{title}_fs_pushers.csv"
    pusher_list = uf.import_csv(file)
    pusher_dict = convert_to_dict(pusher_list)

    exportable = []
    for ds in pusher_dict.keys():
        for t in pusher_dict[ds].keys():
            for row in pusher_dict[ds][t]:
                num_articles = get_num_articles(row[0], ds, t, title)
                exportable.append([ds, t, row[0], int(row[1])/num_articles])
    uf.export_nested_list(f"{title}_fs_relative_to_newspapers.csv", exportable)

def find_absolute_top_pushers(top_pushers):
    by_topic = {}
    by_year = {}
    for ds in top_pushers.keys():
        by_year[ds] ={}
        for t in top_pushers[ds].keys():
            if t not in by_topic.keys():
                by_topic[t] = {}
            for elt in top_pushers[ds][t]:
                if elt[0] not in by_topic[t].keys():
                    by_topic[t][elt[0]]=elt[1]
                else:
                    by_topic[t][elt[0]] += elt[1]

                if elt[0] not in by_year[ds].keys():
                    by_year[ds][elt[0]] = elt[1]
                else:
                    by_year[ds][elt[0]] += elt[1]
    for t in by_topic.keys():
        by_topic[t] = max(by_topic[t], key=by_topic[t].get)
    for y in by_year.keys():
        by_year[y] = max(by_year[y] , key=by_year[y] .get)
    return by_topic, by_year

def find_absolute_top_relative(relative_dict):
    by_topic = {}
    by_year = {}
    for ds in relative_dict.keys():
        by_year[ds] = {}
        for t in relative_dict[ds].keys():
            if t not in by_topic.keys():
                by_topic[t] = {}
            for elt in relative_dict[ds][t]:
                if elt[0] not in by_topic[t].keys():
                    by_topic[t][elt[0]] = [elt[1]]
                else:
                    by_topic[t][elt[0]].append( elt[1])

                if elt[0] not in by_year[ds].keys():
                    by_year[ds][elt[0]] = [elt[1]]
                else:
                    by_year[ds][elt[0]].append(elt[1])
        for n in by_year[ds].keys():
            by_year[ds][n] = sum(by_year[ds][n])/len(by_year[ds][n])
    for t in by_topic.keys():
        for n in by_topic[t].keys():
            by_topic[t][n] = sum(by_topic[t][n])/len(by_topic[t][n])

    for t in by_topic.keys():
        by_topic[t] = max(by_topic[t], key=by_topic[t].get)
    for y in by_year.keys():
        by_year[y] = max(by_year[y] , key=by_year[y] .get)
    return by_topic, by_year


def final_summary(title):
    top_pushers_data = uf.import_csv(f"{title}_fs_pushers.csv")
    rel_to_news_data = uf.import_csv(f"{title}_fs_relative_to_newspapers.csv")

    top_pushers = convert_to_dict(top_pushers_data)
    rel_to_news = convert_to_dict(rel_to_news_data)

    tp_by_topic, tp_by_year = find_absolute_top_pushers(top_pushers)
    rel_by_topic, rel_by_year = find_absolute_top_relative(rel_to_news)

    exportable_topic = [[f'Top Pusher By Topic: {title}'],
                        ['Topic',"Absolute","Relative"]]
    for k in tp_by_topic.keys():
        exportable_topic.append([k, tp_by_topic[k],rel_by_topic[k]])

    exportable_year = [[f'Top Pusher By Year: {title}'],
                        ['Topic',"Absolute","Relative"]]
    for k in tp_by_year.keys():
        exportable_year.append([k, tp_by_year[k],rel_by_year[k]])

    uf.export_nested_list(f"{title}_top_pusher_by_topic.csv",exportable_topic)
    uf.export_nested_list(f"{title}_top_pusher_by_year.csv",exportable_year)
    print('check')


cosine_97 = "no_sent/cosine_97/"
cosine_98 = "no_sent/cosine_98/"

get_relative_to_marginal_top_pushers(f"{cosine_97}20", marg_row=3)
get_relative_to_marginal_top_pushers(f"{cosine_97}30", marg_row=4)
get_relative_to_marginal_top_pushers(f"{cosine_98}20", marg_row=5)
get_relative_to_marginal_top_pushers(f"{cosine_98}30", marg_row=6)

get_num_newspaper_appearances(kmeans_folder=kmeans_97_20,title=f"{cosine_97}20")
get_num_newspaper_appearances(kmeans_folder=kmeans_97_30,title=f"{cosine_97}30")
get_num_newspaper_appearances(kmeans_folder=kmeans_98_20,title=f"{cosine_98}20")
get_num_newspaper_appearances(kmeans_folder=kmeans_98_30,title=f"{cosine_98}30")

get_relative_to_articles_top_pushers(f"{cosine_97}20")
get_relative_to_articles_top_pushers(f"{cosine_97}30")
get_relative_to_articles_top_pushers(f"{cosine_98}20")
get_relative_to_articles_top_pushers(f"{cosine_98}30")


final_summary(f"{cosine_97}20")
final_summary(f"{cosine_97}30")
final_summary(f"{cosine_98}20")
final_summary(f"{cosine_98}30")


