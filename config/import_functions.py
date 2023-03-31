import json
from config import pipeline_types as t
import pickle
from pickle import UnpicklingError


def import_pipeline_data(file, as_dict: bool, typing_type):
    if file.endswith('.json') is not True:
        raise Exception(f'ERROR: {file} should be a .json file')
    with open(file, 'r') as j:
        content = json.loads(j.read())['content']
        if as_dict == True:
            return content  # DEUBG: Make sure this works
        if as_dict == False:
            imported_content = []
            if typing_type == t.Sentiment_Instance:
                for elt in content:
                    parsed = typing_type.parse_obj(elt)
                    imported_content.append(parsed)
                return imported_content
            if isinstance(content[0],list):
                for art in content:
                    for item in art:
                        try:
                            parsed = typing_type.parse_obj(item)
                        except t.ValidationError:
                            print(f'Unable to parse {item}\n')
                            continue
                        imported_content.append(parsed)
            else:
                for art in content:
                    try:
                        parsed = typing_type.parse_obj(art)
                    except t.ValidationError:
                        print(f'Unable to parse {art}\n')
                        continue
                    imported_content.append(parsed)
            return imported_content  # DEBUG: Make sure this works


def import_binary_relation_data(file: str, as_dict: bool):
    content = import_pipeline_data(file=file, as_dict=as_dict, typing_type=t.OpenIEResponse)
    return content


def import_SRO_data_from_file(file: str, as_dict: bool):
    content = import_pipeline_data(file=file, as_dict=as_dict, typing_type=t.SRO_Instance)
    # if as_dict==True: returns 2000 lists of dicts (one row for each list, many dicts for each tuple in the sent)
    # if as_dict==False: return flat list of SRO_Instances
    return content


def import_sentiment_data_from_file(file: str, as_dict:bool):
    content = import_pipeline_data(file=file, as_dict=as_dict,typing_type=t.Sentiment_Instance)
    return content


def import_initial_concepts_data_from_file(file: str):
    if file.endswith('.json') is not True:
        raise Exception(f'ERROR: {file} should be a .json file')
    with open(file, 'r') as j:
        content = json.loads(j.read())['content']
        return content

def import_embedding_triplet_from_file(file:str,as_dict:bool):
    # content = import_pipeline_data(file=file, as_dict=as_dict, typing_type=t.EmbeddingTriplet)
    # Can't use that^ because its a pkl file not a json

    if file.endswith('.pkl') is not True:
        raise Exception(f'ERROR: {file} should be a .pkl file')

    with open(file, "rb") as f:
        try:
            pkl_file = pickle.load(f)
        except UnpicklingError:
            print(f'ERROR: Unpickling error for {file}')
            return
        f.close()
        if as_dict == True:
            return pkl_file
        if as_dict == False:
            imported_content = []
            for elt in pkl_file:
                try:
                    parsed = t.EmbeddingTriplet.parse_obj(elt)
                except:
                    print(f'Unable to parse {elt}\n')
                    continue
                imported_content.append(parsed)

            return imported_content # DEBUG: check that this works
    print('ERROR')
    return

