from NewsSentiment import TargetSentimentClassifier
import NewsSentiment.customexceptions
import universal_functions as uf
import glob
import json
import time
import re
from typing import List

from NarrativeExtractionPipeline.config import import_functions as imp
from NarrativeExtractionPipeline.config import pipeline_types as t

tsc = TargetSentimentClassifier()  # initialize classifier


def get_sentiment_towards_subject(sro_tuple: t.SRO_Instance) -> int:
    # Break the sentence into [before_subject, subject, after_subject]
    subj_start, subj_end = sro_tuple.subjectSpan
    before_subject = " ".join(sro_tuple.tokenized_sentence[:subj_start])
    subject = sro_tuple.subject
    after_subject = " ".join(sro_tuple.tokenized_sentence[subj_end:])

    # Classify the sentiment of the sentence
    try:
        sentiment = tsc.infer_from_text(before_subject, subject, after_subject)
    except NewsSentiment.customexceptions.TooLongTextException:
        return 999
    except NewsSentiment.customexceptions.TargetNotFoundException:
        return 999
    # Negative: 0, neutral: 1, positive: 2
    return sentiment[0]['class_id'] # Return the associated number value


def find_previous_checkpoints(filename:str)->List:
    dataset_name = uf.get_dataset_id(filename)
    sentiment_files = [x for x in glob.glob('Sentiment_Instances' + "/*.json")]
    highest_checkpoint = [0, '']
    for file in sentiment_files: # look through previous sentiment files
        if dataset_name in file: # if there's a file from the same dataset...
            if 'checkpoint' not in file:
                return ['complete']
            regex = r"(?<=\_Sentiment_)(.*?)(?=\_ch)"
            checkpoint = int(re.findall(regex, file)[0])
            if checkpoint > highest_checkpoint[0]: # look to see how far the highest file found got
                highest_checkpoint[0] = checkpoint
                highest_checkpoint[1] = file
    return highest_checkpoint # [checkpoint number, file name ]


def collect_instances_from_same_sentence(dataset:List[t.SRO_Instance], index:int):
    sent_id = dataset[index].sentence_id
    subject = dataset[index].subject
    collected_instances = []
    for i in range(index,len(dataset)): # Starting at the given index, look for matching subjects/ sent ids
        if dataset[i].sentence_id == sent_id and dataset[i].subject == subject:
            collected_instances.append(dataset[i])
        if dataset[i].sentence_id > sent_id:
            break # end the for loop as soon as we have finished going through the given sentence id
    return collected_instances # return all instances w the same subject and sent id


def run_sentiment_analyzer(filename):
    # Check if there are already checkpoints available
    highest_checkpoint = find_previous_checkpoints(filename)
    if highest_checkpoint == ['complete']:
        return 'complete'

    content = imp.import_SRO_data_from_file(filename, as_dict=False)

    output,completed_sentiment = [],[]
    if highest_checkpoint[1] != '':
        prev_data = imp.import_sentiment_data_from_file(highest_checkpoint[1], as_dict=True)
        output += prev_data
    print(f'    Starting at {highest_checkpoint[0]}')
    a = time.time()
    for i in range(highest_checkpoint[0] + 1, len(content)):
        if [content[i].sentence_id,content[i].subject] in completed_sentiment:
            continue

        same_sent_inst = collect_instances_from_same_sentence(content, i)

        sentiment = get_sentiment_towards_subject(content[i]) # classify the sentiment for that sent/ subj

        for inst in same_sent_inst:
            inst_dict = inst.dict()
            inst_dict['sentiment'] = sentiment
            output.append(inst_dict)

        completed_sentiment.append([content[i].sentence_id,content[i].subject])
        # sentiment_instance = content[i].dict()
        # sentiment_instance['sentiment'] = sentiment
        # output.append(sentiment_instance)

        if str(i).endswith('000'):
            b = time.time()
            print(f"    Has taken {b - a} seconds to run {i} sro_instances\nExporting checkpoint...")
            print(f"    {(i/len(content))*100}% complete")
            to_export = json.dumps({'content': output})
            export_filename = filename.replace("_SRO", f"_Sentiment_{i}_checkpoint").replace('SRO_Instances',
                                                                                         'Sentiment_Instances')
            uf.export_as_json(export_filename, to_export) # DEBUG: check that the filename is correct
    return output


if __name__ == '__main__':
    SRO_files = [x for x in glob.glob(
        'C:\\Users\\khahn\\Documents\\Github\\Thesis\\NarrativeExtractionPipeline\\SRO_Instances' + "/*.json") if
                 'checkpoint' not in x]
    for file in SRO_files[19:]:
        print(f'Running {file}...')
        response = run_sentiment_analyzer(file)
        if response == 'complete' :
            print('    Already complete')
            continue
        to_export = json.dumps({'content': response})
        export_filename = file.replace("_SRO", "_Sentiment").replace('SRO_Instances', 'Sentiment_Instances')
        uf.export_as_json(export_filename, to_export)