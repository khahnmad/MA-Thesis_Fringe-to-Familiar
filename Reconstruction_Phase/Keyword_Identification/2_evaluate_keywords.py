"""
Second step

"""
import universal_functions as uf
import json
from config import import_functions as imp
import random


# Functions
def compile_candidate_keywords()->dict:
    """ Get keywords from article classification and format them"""

    classification = uf.import_json_content("Keyword_Article_Classification.json")

    # Create list of unique keywords per narrative
    candidate_keywords = {}
    for obj in classification:
        if obj['labels']=='Other':
            continue
        for key in obj['labels'].keys():
            try:
                keywords = obj['labels'][key]['keywords'].split(';')

            except AttributeError:
                keywords = obj['labels'][key]['keywords']

            if key not in candidate_keywords.keys():
                candidate_keywords[key]=keywords
            else:
                for word in keywords:
                    if word not in candidate_keywords[key]:
                        candidate_keywords[key].append(word)
    candidate_keywords={k:candidate_keywords[k] for k in candidate_keywords.keys() if k!="Other"}
    return candidate_keywords


def find_invalid_keywords(keyword_matches)->list:
    """ Remove keywords that have already been thoroughly tested"""
    results = {}
    to_remove = []
    for obj in keyword_matches:
        if obj['word']not in results.keys():
            results[obj['word']] = [obj['evaluation']]
        else:
            results[obj['word']].append(obj['evaluation'])
    for k in results.keys():
        incorrect = [int(x) for x in results[k] if x =='-1' and x!='']
        correct = [int(x) for x in results[k] if x =='1' and x!='']
        try:
            perc_correct = len(correct)/(len(incorrect)+len(correct))
        except ZeroDivisionError:
            perc_correct=0
        print(f"{k}:{perc_correct} out of {(len(incorrect)+len(correct))} samples")
        if len(incorrect)+len(correct)>7 and perc_correct <.5:
            to_remove.append(k)

        if len(results[k])> 10:
            to_remove.append(k)
    all_keywords = list(results.keys())
    print(f"{len(to_remove)}/ {len(all_keywords )} keywords have been removed")
    return to_remove


def find_matching_sro_triplets(candidate_keywords,num):
    """ Evaluate the keywords from the article classification """
    sro_locs = uf.get_files_from_folder(str(uf.repo_loc / 'Deconstruction_Phase') + "SRO_Instances",'json')
    keyword_matches=uf.import_json_content("Keyword_SRO_matches.json")

    invalid_keywords = find_invalid_keywords(keyword_matches)

    for i in range(len(sro_locs)): # Iterate through the sros
        loc = random.choice(sro_locs)
        dataset_name = uf.get_dataset_id(loc)

        sro_data = imp.import_SRO_data_from_file(loc,as_dict=False)
        for narr in candidate_keywords.keys():

            keywords = [x for x in candidate_keywords[narr] if x not in invalid_keywords]

            for i in range(num):

                for keyword in keywords:
                    chosen_index = random.randint(0,len(sro_data)-1)
                    obj = sro_data[chosen_index]

                    if keyword in obj.subject.lower() or keyword in obj.relation.lower() or keyword in obj.object.lower():
                        if keyword in [x.lower() for x in obj.tokenized_sentence] or ' ' in keyword:
                            found_match = {'dataset_name':dataset_name,
                                           'article_id':obj.article_id,
                                           'sentence_id':obj.sentence_id,
                                           'subject':obj.subject,
                                           'relation':obj.relation,
                                           'object':obj.object,
                                           'tokenized_sentence':obj.tokenized_sentence,
                                           'narrative':narr,
                                           'word':keyword}
                            if found_match not in keyword_matches:
                                print(
                                    f"Narrative:{found_match['narrative']}\nWord:{found_match['word']}\nSentence:\n{' '.join(found_match['tokenized_sentence'])}")
                                evaluation = input("Input: Matches(1), Doesn't Match(-1), Unclear(0)")
                                if evaluation=='quit':
                                    a_content = json.dumps({'content': keyword_matches})
                                    uf.export_as_json(f"Keyword_SRO_matches.json", a_content)
                                    return keyword_matches
                                found_match['evaluation']=evaluation
                                if found_match not in keyword_matches:
                                    keyword_matches.append(found_match)
    a_content = json.dumps({'content': keyword_matches})
    uf.export_as_json(f"Keyword_SRO_matches.json", a_content)
    return keyword_matches


## ACTION ##
candidates = compile_candidate_keywords()
matches = find_matching_sro_triplets(candidates,30000)