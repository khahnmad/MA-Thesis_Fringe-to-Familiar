import universal_functions as uf
from Results.locations import *
from collections import Counter

def find_overlap_coefficient(X:list,Y:list):
    if min(len(X), len(Y)) == 0:
        return 0
    return len(set(X).intersection(set(Y))) / min(len(X), len(Y))


def get_NEs(cluster_ids, kmeans, dataset_name, topic):
    kmeans_loc = [x for x in kmeans if f"\\{dataset_name}" in x][0]
    kmeans_data = uf.import_pkl_file(kmeans_loc)
    types = ["NATIONALITY","PERSON","MISC","COUNTRY","RELIGION","ORGANIZATION","TITLE","STATE_OR_PROVINCE"]
    NEs = []
    for cluster_id in cluster_ids:
        cluster_elts = [x['entity_location'] for x in kmeans_data[topic]['narratives_classified'] if x['cluster_index'] == int(cluster_id)]
        for elt in cluster_elts:
            if len(elt)<1:
                continue
            for k in elt.keys():
                for item in elt[k]:
                    if item["ner"] in types:
                        NEs.append([item['text'], item['ner'],k])

    return NEs

def find_NEs(mainstream_data, kmeans_folder, title):
    named_entities = {}
    for ds in mainstream_data.keys():
        named_entities[ds] ={}
        for t in mainstream_data[ds].keys():

            ne = get_NEs(mainstream_data[ds][t], kmeans_folder, ds, t)
            named_entities[ds][t] = ne
    uf.content_json_export(f"{title}_FR_named_entities.json",named_entities)



def find_fs_NEs(fs_files,kmeans_folder, title):
    named_entities= {}
    for file in fs_files:
        data = uf.import_json_content(file)
        datset_name = uf.get_dataset_id(file)
        named_entities[datset_name] ={}

        for topic in data.keys():
            named_entities[datset_name][topic] = {}
            for cluster_id in data[topic].keys():
                for item in data[topic][cluster_id]:
                    if item[0] not in named_entities[datset_name][topic].keys():
                        named_entities[datset_name][topic][item[0]] = {'cluster_ids':[]}
                    named_entities[datset_name][topic][item[0]]['cluster_ids'].append(item[1])

    for ds in named_entities.keys():
        for t in named_entities[ds].keys():
            for p in named_entities[ds][t].keys():
                entities = get_NEs(cluster_ids=named_entities[ds][t][p]['cluster_ids'], kmeans=kmeans_folder,dataset_name=p,
                        topic=t)
                named_entities[ds][t][p] = entities
    uf.content_json_export(f"{title}_FS_named_entities.json",named_entities)



# Find top absolute FR named entities
def top_absolute_fr_nes(title):
    data = uf.import_json_content(f"{title}_FR_named_entities.json")

    by_topic = [['Topic','Entity','Frequency']]
    by_year = [['Year','Entity','Frequency']]
    overall = [['Dataset','Topic','Entity','Frequency']]
    topic_dict ={}
    year_dict = {}
    for ds in data.keys():
        if ds not in year_dict.keys():
            year_dict[ds] = []

        for t in data[ds].keys():

            if t not in topic_dict.keys():
                topic_dict[t] = []
            topic_dict[t] += [x[0] for x in data[ds][t]]

            year_dict[ds] += [x[0] for x in data[ds][t]]

            counter = Counter([x[0] for x in data[ds][t]])
            for c in counter.keys():
                overall.append([ds, t, c, counter[c]])

    for k in topic_dict.keys():
        counter = Counter(topic_dict[k])
        for c in counter.keys():
            by_topic.append([k, c, counter[c]])

    for k in year_dict.keys():
        counter = Counter(year_dict[k])
        for c in counter.keys():
            by_year.append([k, c, counter[c]])

    uf.export_nested_list(f"{title}_FR_NEs_overall.csv",overall)
    uf.export_nested_list(f"{title}_FR_NEs_by_topic.csv",by_topic)
    uf.export_nested_list(f"{title}_FR_NEs_by_year.csv",by_year)



# Find top absolute FR named entities
def top_absolute_fs_nes(title):
    data = uf.import_json_content(f"{title}_FS_named_entities.json")

    by_topic = [['Topic','Entity','Frequency']]
    by_year = [['Year','Entity','Frequency']]
    overall = [['Dataset','Topic','Entity','Frequency']]
    topic_dict ={}
    year_dict = {}
    for ds in data.keys():
        if ds not in year_dict.keys():
            year_dict[ds] = []

        for t in data[ds].keys():

            if t not in topic_dict.keys():
                topic_dict[t] = []

            part_ds_nes = []
            for part_ds in data[ds][t].keys():
                topic_dict[t] += [x[0] for x in data[ds][t][part_ds]]

                year_dict[ds] += [x[0] for x in data[ds][t][part_ds]]

                part_ds_nes += [x[0] for x in data[ds][t][part_ds]]
            counter = Counter(part_ds_nes)
            for c in counter.keys():
                overall.append([ds, t, c, counter[c]])

    for k in topic_dict.keys():
        counter = Counter(topic_dict[k])
        for c in counter.keys():
            by_topic.append([k, c, counter[c]])

    for k in year_dict.keys():
        counter = Counter(year_dict[k])
        for c in counter.keys():
            by_year.append([k, c, counter[c]])

    uf.export_nested_list(f"{title}_FS_NEs_overall.csv",overall)
    uf.export_nested_list(f"{title}_FS_NEs_by_topic.csv",by_topic)
    uf.export_nested_list(f"{title}_FS_NEs_by_year.csv",by_year)

# find_NEs(fs_nosent_97_20_main, kmeans_97_20,"no_sent/cosine_97/20")
# find_NEs(fs_nosent_97_30_main, kmeans_97_30,"no_sent/cosine_97/30")
# find_NEs(fs_nosent_98_20_main, kmeans_98_20,"no_sent/cosine_98/20")
# find_NEs(fs_nosent_98_30_main, kmeans_98_30,"no_sent/cosine_98/30")


# find_fs_NEs(fs_97_20_nosent, kmeans_97_20, 'no_sent/cosine_97/20')
# find_fs_NEs(fs_97_30_nosent, kmeans_97_30, 'no_sent/cosine_97/30')
# find_fs_NEs(fs_98_20_nosent, kmeans_98_20, 'no_sent/cosine_98/20')
# find_fs_NEs(fs_98_30_nosent, kmeans_98_30, 'no_sent/cosine_98/30')

# top_absolute_fr_nes( 'no_sent/cosine_97/20')
# top_absolute_fr_nes( 'no_sent/cosine_97/30')
# top_absolute_fr_nes( 'no_sent/cosine_98/20')
# top_absolute_fr_nes( 'no_sent/cosine_98/30')

# top_absolute_fs_nes( 'no_sent/cosine_97/20')
# top_absolute_fs_nes( 'no_sent/cosine_97/30')
# top_absolute_fs_nes( 'no_sent/cosine_98/20')
# top_absolute_fs_nes( 'no_sent/cosine_98/30')

def find_marg_fs_ne_overlap(marg_files, kmeans_folder, title):
    named_entities = {}

    for marg_file in marg_files:
        data = uf.import_json_content(marg_file)

        for ds in data.keys():
            named_entities[ds] = {}

            for t in data[ds].keys():
                if t not in named_entities.keys():
                    named_entities[ds][t] = {}

                for marg_cluster_id in data[ds][t].keys():
                    ne = get_NEs([marg_cluster_id], kmeans_folder, ds, t)
                    named_entities[ds][t][marg_cluster_id] = [x[0] for x in ne]

    direct_files = [marg_file.replace('marginal_NEs','direct_NEs') for marg_file in marg_files]
    for file in direct_files:
        dir_data = uf.import_json_content(file)

        for d_ds in dir_data.keys():
            for topic in dir_data[d_ds].keys():
                for cluster_id in dir_data[d_ds][topic].keys():
                    fs_nes = []
                    for fs_ds in dir_data[d_ds][topic][cluster_id].keys():
                        fs_cluster_ids = list(dir_data[d_ds][topic][cluster_id][fs_ds].keys())
                        fs_nes += get_NEs(cluster_ids=fs_cluster_ids,kmeans=kmeans_folder,dataset_name=fs_ds, topic=topic)
                    overlap_coef = find_overlap_coefficient(named_entities[d_ds][topic][cluster_id],
                                                            [x[0] for x in fs_nes])
                    named_entities[d_ds][topic][cluster_id] = overlap_coef
    uf.content_json_export(export_name=f"{title}_marg_fs_ne_overlap.json",data=named_entities)



def summarize_overlap(title):
    data = uf.import_json_content(f"{title}_marg_fs_ne_overlap.json")

    by_topic, by_year = [],[]
    topic_dict, year_dict ={},{}
    for ds in data.keys():
        if ds not in year_dict.keys():
            year_dict[ds] = []
        for t in data[ds].keys():
            if t not in topic_dict.keys():
                topic_dict[t] = []

            topic_dict[t]+=list(data[ds][t].values())
            year_dict[ds]+=list(data[ds][t].values())

    for t in topic_dict.keys():
        try:
            by_topic.append([t, sum(topic_dict[t])/len(topic_dict[t])])
        except ZeroDivisionError:
            by_topic.append([t,0])

    for ds in year_dict.keys():
        try:
            by_year.append([ds, sum(year_dict[ds])/len(year_dict[ds])])
        except ZeroDivisionError:
            by_year.append([ds,0])

    uf.export_nested_list(f"{title}_overlap_by_topic.csv", by_topic)
    uf.export_nested_list(f"{title}_overlap_by_year.csv",by_year)


def find_overlapping_words(mainstream_data, kmeans_folder, fs_files, title):
    named_entities = {}
    for ds in mainstream_data.keys():
        named_entities[ds] = {}
        for t in mainstream_data[ds].keys():
            if t not in named_entities.keys():
                named_entities[ds][t] = {}
            for cluster_id in mainstream_data[ds][t]:
                ne = get_NEs([cluster_id], kmeans_folder, ds, t)
                named_entities[ds][t][cluster_id] = [x[0] for x in ne]

    for file in fs_files:
        data = uf.import_json_content(file)
        datset_name = uf.get_dataset_id(file)

        for topic in data.keys():

            for cluster_id in data[topic].keys():

                if cluster_id in named_entities[datset_name][topic].keys():
                    fs_nes = []
                    for item in data[topic][cluster_id]:
                        fs_nes += get_NEs(cluster_ids=[item[1]], kmeans=kmeans_folder, dataset_name=item[0],
                                          topic=topic)
                    overlapping_words = set(named_entities[datset_name][topic][cluster_id]).intersection(set([x[0] for x in fs_nes]))
                    named_entities[datset_name][topic][cluster_id] = list(overlapping_words)
    uf.content_json_export(export_name=f"{title}_overlapping_words.json", data=named_entities)



find_marg_fs_ne_overlap(all_narr_97_20, kmeans_97_20,'no_sent/cosine_97/20')
find_marg_fs_ne_overlap(all_narr_97_30, kmeans_97_30,'no_sent/cosine_97/30')
find_marg_fs_ne_overlap(all_narr_98_20, kmeans_98_20,'no_sent/cosine_98/20')
find_marg_fs_ne_overlap(all_narr_98_30, kmeans_98_30,'no_sent/cosine_98/30')

summarize_overlap('no_sent/cosine_97/20')
summarize_overlap('no_sent/cosine_97/30')
summarize_overlap('no_sent/cosine_98/20')
summarize_overlap('no_sent/cosine_98/30')


# find_overlapping_words(fs_nosent_97_20_main, kmeans_97_20,fs_97_20_nosent,'no_sent/cosine_97/20')
# find_overlapping_words(fs_nosent_97_30_main, kmeans_97_30,fs_97_30_nosent,'no_sent/cosine_97/30')
# find_overlapping_words(fs_nosent_98_20_main, kmeans_98_20,fs_98_20_nosent,'no_sent/cosine_98/20')
# find_overlapping_words(fs_nosent_98_30_main, kmeans_98_30,fs_98_30_nosent,'no_sent/cosine_98/30')