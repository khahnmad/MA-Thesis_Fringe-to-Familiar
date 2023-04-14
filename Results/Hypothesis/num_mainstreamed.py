
from Results.locations import *
import pandas as pd


def get_df(all_narr_folder,title):
    results = []
    for file in all_narr_folder:
        data = uf.import_json_content(file)
        ds_name = list(data.keys())[0]

        for t in data[ds_name].keys():
            num_marg_narratives = len(data[ds_name][t])
            results.append([ds_name, t, num_marg_narratives])
    df = pd.DataFrame(results, columns=['Dataset','Topic',title])
    return df

def get_num_direct_mainstreamed():
    num_97_20 = get_df(dir_narr_97_20, "97, 20")
    num_97_30 = get_df(dir_narr_97_30, "97, 30")
    num_98_20 = get_df(dir_narr_98_20, "98, 20")
    num_98_30 = get_df(dir_narr_98_30, "98, 30")

    merged = pd.merge(num_97_20, num_97_30, on=['Dataset',"Topic"], how='outer')
    merged = pd.merge(merged, num_98_20, on=['Dataset',"Topic"],how='outer')
    merged = pd.merge(merged, num_98_30, on=['Dataset',"Topic"],how='outer')

    merged.to_csv('Num_Direct_Mainstreamed_Narratives.csv')


def get_num_periph_mainstreamed():
    num_97_20 = get_df(periph_narr_97_20, "97, 20")
    num_97_30 = get_df(periph_narr_97_30, "97, 30")
    num_98_20 = get_df(periph_narr_98_20, "98, 20")
    num_98_30 = get_df(periph_narr_98_30, "98, 30")

    merged = pd.merge(num_97_20, num_97_30, on=['Dataset', "Topic"], how='outer')
    merged = pd.merge(merged, num_98_20, on=['Dataset', "Topic"], how='outer')
    merged = pd.merge(merged, num_98_30, on=['Dataset', "Topic"], how='outer')

    merged.to_csv('Num_Periph_Mainstreamed_Narratives.csv')

get_num_direct_mainstreamed()
get_num_periph_mainstreamed()