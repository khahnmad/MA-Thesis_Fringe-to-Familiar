"""
FINAL STEP in keyword identification:

- Takes the "Keyword_SRO_matches.json" file from the manual evaluation and filters through to identify the valid
  keywords
"""
import universal_functions as uf
import json

# Import manual evaluation file
matches = uf.import_json_content('../../Classification_data/Seedwords/Keyword_SRO_matches.json')

# Sort the evaluations
keyword_dict = {}
for elt in matches:
    narr =  elt['narrative']
    word = elt['word']
    if narr not in keyword_dict.keys():
        keyword_dict[narr] = {}
    if word not in keyword_dict[narr].keys():
        keyword_dict[narr][word]=[]
    keyword_dict[narr][word].append(elt['evaluation'])

# Filter through the evaluations and save the valid ones
valid_keywords = {}
for narr in keyword_dict.keys():
    valid_keywords[narr]=[]
    for word in keyword_dict[narr].keys():
        correct = [int(x) for x in keyword_dict[narr][word] if x =='1']
        incorrect = [int(x) for x in keyword_dict[narr][word] if x =='-1']
        try:
            perc_correct = len(correct)/(len(correct)+len(incorrect))
        except ZeroDivisionError:
            perc_correct = 0
        total_samples = len(keyword_dict[narr][word])
        if perc_correct >0.95 and total_samples >= 5:
            valid_keywords[narr].append(word)

# Export the evaluation
a_content = json.dumps({'content': valid_keywords})
uf.export_as_json(f"valid_keywords.json", a_content)


