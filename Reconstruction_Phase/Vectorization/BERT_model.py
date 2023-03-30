# Source: https://mccormickml.com/2019/05/14/BERT-word-embeddings-tutorial/#contents
import torch # strikes a balance between high-level APIs and tensorflow code
from transformers import BertTokenizer, BertModel
import pickle
from typing import List
import universal_functions as uf

# GLOBAL
# using the basic model from transformers that has no specific output task
# "from_pretrained" calls from internt
model = BertModel.from_pretrained('bert-large-cased',
                              output_hidden_states = True, # Whether the model returns all hidden-states.
                              )
model.eval() # turns off dropout regularization - feed-forward operation

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased') # WordPiece tokenizer

embeddings_dir = uf.repo_loc / 'Reconstruction_Phase/Vectorization/Embeddings'

def create_segment_ids(tokens:List[str])->List[int]:
    # Converts a list of tokens w CLS & SEP into segment ids for 1 to three "sentences"
    segments_ids = []
    starting_point = 0
    for i in range(len(tokens)):
        if tokens[i] == '[SEP]':
            segments_ids.append(0)
            starting_point = i + 1
            break
        segments_ids.append(0)

    for i in range(starting_point, len(tokens)):
        if tokens[i] == '[SEP]':
            segments_ids.append(1)
            starting_point = i + 1
            break
        segments_ids.append(1)

    for i in range(starting_point, len(tokens)):
        segments_ids.append(2)
    return segments_ids




def generate_text_for_whole_triplet(sro_obj:dict)->dict:
    marked_text = f"[CLS] {sro_obj['subject']} {sro_obj['relation']} {sro_obj['object']} [SEP]"
    text = f"{sro_obj['subject']} {sro_obj['relation']} {sro_obj['object']}"
    return {'marked_text': marked_text, 'label_text': text}




def vectorize_triplet(prepped_text:dict):
    """

    :param prepped_text: 'marked_text': text with CLS & SEP, 'label_text': original text
    :return:
    """
    tokenized_text = tokenizer.tokenize(prepped_text['marked_text'])[:510] # Tokenize the BERT tokenizer.
    indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text) # Map the token strings to their vocabulary indices.
    segments_ids = create_segment_ids(tokenized_text)

    # Convert inputs to PyTorch tensors as required by bert pytorch interface
    tokens_tensor = torch.tensor([indexed_tokens])
    segments_tensors = torch.tensor([segments_ids])

    # Collect hidden states from all 24 layers
    with torch.no_grad(): # reduces memory consumption by not constructing the compute graph
        outputs = model(tokens_tensor, segments_tensors)
        hidden_states = outputs[2] # index could change if model is reconfigured

    token_embeddings = torch.stack(hidden_states, dim=0)
    token_embeddings = torch.squeeze(token_embeddings, dim=1)
    token_embeddings = token_embeddings.permute(1,0,2)

    # token_vecs_cat = []
    # for token in token_embeddings:
    #     cat_vec = torch.cat((token[-1], token[-2], token[-3], token[-4]), dim=0)
    #     token_vecs_cat.append(cat_vec)

    token_vecs_sum = []
    for token in token_embeddings:
        sum_vec = torch.sum(token[-4:], dim=0)
        token_vecs_sum.append(sum_vec)

    token_vecs = hidden_states[-2][0]
    # Calculate the average of all 22 token vectors.
    embedding = torch.mean(token_vecs, dim=0)
    return embedding, prepped_text['label_text']




def generate_embeddings_for_dataset(sro_data,mode, starting_point, embeddings, dataset_name):

    print(f'    Starting at {starting_point}...')
    for i in range(starting_point,len(sro_data)):

        prepped_text = generate_text_for_whole_triplet(sro_data[i])
        # sro_dict = dict(sro_data[i])
        try:
            e, t = vectorize_triplet(prepped_text) # TODO: can remove redundant "t"
        except IndexError:
            e = None
        except RuntimeError:
            e = None
        sro_data[i]['embedding'] = e
        embeddings.append(sro_data[i])

        if str(i).endswith("000"):
            print(f'Dumping checkpoint {i} to pickle file ({(i/len(sro_data))*100} done)....')
            export_name = embeddings_dir / f"{dataset_name}_embeddings_{i}_checkpoint.pkl"
            with open(export_name, "wb") as f:
                pickle.dump(embeddings, f)

    return embeddings
