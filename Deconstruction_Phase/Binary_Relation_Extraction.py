# command line to open the server:
# cd C:\Users\khahn\Documents\Github\Thesis\Coreference_dependencyTree\content\stanford-corenlp-4.5.1\stanford-corenlp-4.5.1
# java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 50000

from pycorenlp import StanfordCoreNLP # model

import universal_functions as uf
import json
import glob
import re
import time
from typing import List

from config import pipeline_types as t, import_functions as imp

"""
Should apply some kind of cleaning to select unique and high-precision extractions, like in Tangherlini
at the very least, lowercasing of the args and rels
Todo
- stop printing the article each time in the command line 
"""
nlp = StanfordCoreNLP('http://localhost:9000')


def get_named_entities(sro_instance:t.OpenIEResponse, entity_mentions:List[dict])->dict:
    # find the text and location of named entities in the triplet, if there are any
    entity_location = {}
    for entity_mention in entity_mentions:

        entity_start = entity_mention["tokenBegin"]
        entity_end = entity_mention["tokenEnd"]

        spans = [sro_instance.subjectSpan, sro_instance.relationSpan, sro_instance.objectSpan]
        span_conversion = {0:'Subject',1:"Relation",2:"Object"}

        for i in range(len(spans)):
            # given_span = span
            if spans[i][0] <= entity_start <= spans[i][1] and spans[i][0] <= entity_end <= spans[i][1]:
                # The entity is within the span
                sent_part = span_conversion[i]
                # NOTE: it's possible to get the confidence for this ner prediction
                if sent_part not in entity_location.keys():
                    entity_location[sent_part] = [{'text': entity_mention['text'],
                                                   f"{sent_part}Span": [entity_start, entity_end],
                                                   'ner': entity_mention["ner"]}]
                else:
                    entity_location[sent_part].append({'text': entity_mention['text'],
                                                       f"{sent_part}Span": [entity_start, entity_end],
                                                       'ner': entity_mention["ner"]})
    return entity_location


def extract_SROs(content:t.StanfordModelResponse, article_id:str)->List[dict]:
    # Takes in one document and extracts the SROs from each sentence in the document
    outputs = [] # initialize
    for sent in content.sentences: # iterate through t.SentenceResponse types in the document
        tokenized_sentence = [x['originalText'] for x in sent.tokens] # Create a list of the tokenized text of the sent
        # TODO : check if it's too long - what to do if this is the case?
        if len(tokenized_sentence)>600:
            print(f'sentence is too long: {len(tokenized_sentence)} tokens')
        sent_id = sent.index # num of the sentence in the document

        # Check if there was a successful open ie extraction
        openie_exists = len(sent.openie) > 0
        if openie_exists is False:
            continue
        # Examine the successful extraction
        SROs = sent.openie
        for sro in SROs:  # iterate through the subject-relation-object extractions

            output_instance = sro.dict()  # get the subject, relation, object & their locations in dict format
            output_instance["tokenized_sentence"] = tokenized_sentence
            output_instance['sentence_id']=sent_id
            output_instance["article_id"] = article_id # DEBUG: Check this works

            entity_mentions_exist = len(
                sent.entitymentions) > 0  # Check if there are entity mentions in the sentence
            if entity_mentions_exist is not True:
                continue

            output_instance['entity_location'] = get_named_entities(sro_instance=sro,
                                                                    entity_mentions=sent.entitymentions)
            outputs.append(output_instance)
    return outputs


def call_corenlp_model(article:str, article_id:str)->List[dict]:
    # Call the model
    nlp_response = nlp.annotate(article,
                                properties={"annotators": "tokenize,ssplit,pos,depparse,natlog,openie,coref",
                                            "openie.triple.strict": "False",
                                            "openie.triple.all_nominals": "True",
                                            "outputFormat": "json",
                                            "openie.resolve_coref": "True"
                                            })
    try:
        parsed_response = t.StanfordModelResponse.parse_obj(nlp_response)
    except ValueError:
        error = []
        if isinstance(nlp_response, str):
            print(nlp_response) # TODO: Need a strategy
            error = [f'ERROR for {article_id}: {nlp_response}']
        return error

    # Process the model response
    outputs = extract_SROs(parsed_response, article_id)
    return outputs



def find_previous_runs(prev_exports:List[str], dataset_id:str)->List:
    # Check which files have already been run
    highest_count = [2001, '']
    for ex in prev_exports:
        if f'\\{dataset_id}_SRO_' in ex:
            find_count = r"(?<=\_SRO\_)(.*?)(?=\_checkpoint)"
            count = int(re.findall(find_count, ex)[0])
            if highest_count[0] < count or highest_count[0]==2001:
                highest_count = [count, ex] # highest checkpoint, file loc
        if f'\\{dataset_id}_SRO.json' in ex:
            highest_count[0] = 2000
    return highest_count


if __name__ == '__main__':
    prepped_dataset = uf.load_all_complete_datasets()
    previous_exports = [x for x in glob.glob('SRO_Instances\\' + "/*.json")]

    for file in prepped_dataset:
        dataset_name = uf.get_dataset_id(file) # Get dataset name
        highest_count = find_previous_runs(previous_exports, dataset_name) # Find the highest previous export of this file

        # Initialize variables
        output = []
        starting_point=1

        if highest_count[0] <2000:
            starting_point = highest_count[0]+1
            existing_content = imp.import_binary_relation_data(file=highest_count[1],as_dict=True)
            output+=existing_content
        if highest_count[0]==2000:
            continue

        data = uf.import_csv(file) # length should be 2000

        print(f"Running {file}...")
        print(f"    starting at {starting_point}")
        a= time.time()
        for i in range(starting_point, len(data)):
            print(f"        {i}")
            if i in range(1841,1842):
                print(f"SKIPPING THIS ONE!")
                continue
            output.append(call_corenlp_model(article=data[i][-1], article_id=data[i][0]))
            if str(i).endswith('0'):
                midpoint_export = f"SRO_Instances\\{dataset_name}_SRO_{str(i)}_checkpoint.json"
                export_content = json.dumps({'content': output})
                uf.export_as_json(midpoint_export, export_content)
                c = time.time()
                print(f'    Exporting midpoint: {midpoint_export}')
                print(f"    Took {c-a} seconds to run so far")
        b= time.time()
        print(f"Took {b-a} seconds for {dataset_name} to run")
        export_filename = f"SRO_Instances\\{dataset_name}_SRO.json"
        export_content = json.dumps({'content': output})
        uf.export_as_json(export_filename, export_content)


"""
NOTES:

natlog & openie have to be included in the annotators property to be able to use the flags here:
https://nlp.stanford.edu/software/openie.html

openie depends on the annotators "tokenize,ssplit,pos,depparse"


{
        Subject: str
        Object: str
        Verb: str
        Sentence: str
        Dataset_id: str (ex: Center_2-2016)
        Article_id: int
        Entity_Locations : {Subject:[[start_char, end_char]], Verb: [], Object: []}
        }


The text version (outputFormat: text) makes no sense to parse
"openie.max_entailments_per_clause":"1"
"triple.all_nominals":"True",                       ,
"""
