from googleapiclient.discovery import build
import sys
import urllib.request 
from bs4 import BeautifulSoup
import spacy
from spanbert import SpanBERT
import itertools

def get_text(url):
    text = ""
    try:
        html = urllib.request.urlopen(url)
        htmlParse = BeautifulSoup(html, 'html.parser')
    except urllib.error.HTTPError: 
        return None
    for para in htmlParse.find_all("p"):
        text = text + para.get_text()
    if len(text) == 0:
        return None
    if len(text)>10000:
        text = text[ 0 : 10000 ]
    return text

def process_text(model, text):

    sentence2entities = []

    processed_text = model(text)
    for sent in processed_text.sents:
        named_entities_per_sent = sentence.ents
        sentence2entities.append({"sentence": sent, "named_entities": named_entities_per_sent})

    return sentence2entities

def process_required_entities(sent2ents, required_entity_types):

    sent2ents_processed = []

    for ents_per_sent in sent2ents:
        sent, named_entities_per_sent = ents_per_sent["sentence"], ents_per_sent["named_entities"]
        required_named_entities = [ent for ent in named_entities_per_sent if ent.label_ in required_entity_types]
        sent2ents_processed.append({"sentence": sent, "named_entities": named_entities_per_sent})

    return sent2ents_processed

def process_required_pairs(sent2ents, required_relation_types, spacy2bert):

    required_pairs, required_sents = [], []

    for ents_per_sent in sent2ents:

        sent, named_entities_per_sent = ents_per_sent["sentence"], ents_per_sent["named_entities"]

        required_ents = {}
        pairs_per_sent = {}

        for ent in named_entities_per_sent:
            name, label = ent.text, ent.label_
            if label not in required_ents:
                required_ents[label] = []
            required_ents[label].append(name)

        for relation_type in required_relation_types:
            subj, obj = relation_type
            if subj not in required_ents or obj not in required_ents:
                continue
            subj_ents, obj_ents = required_ents[subj], required_ents[obj]
            relation_indexs = [(i, j) for i in range(len(subj_ents)) for j in range(len(obj_ents))]
            pairs_per_sent[relation_type] = []
            for idx in relation_indexs:
                subj_ent, obj_ent = subj_ents[idx[0]], obj_ents[idx[1]]
                subj_info = (subj_ent.text, spacy2bert[subj_ent.label_], subj_ent.start, subj_ent.end)
                obj_info = (obj_ent.text, spacy2bert[obj_ent.label_], obj_ent.start, obj_ent.end)
                pairs_per_sent[relation_type].append({"tokens": sent, "subj": subj_info, "obj": obj_info})

        if len(pairs_per_sent) != 0:
            required_pairs.append(pairs_per_sent)
            required_sents.append(sent)
    
    return required_pairs, required_sents

def process_relations(model, pairs, sents, confidence_threshold):
    if isinstance(model, 'spanbert.SpanBERT'):
        return extraction_spanbert(model, pairs, confidence_threshold)
    elif isinstance(model, 'method'):
        return extraction_gpt3(model, sents)
    else:
        raise NotImplementedError

def extraction_spanbert(spanbert_model, model, relations, t, required_relation_types):

    required_tuples = set()
    required_tuples_with_scores = {}
    for relations_per_sent in relations:
        relations_pred_per_sent = spanbert_model.predict(relations_per_sent)
        for relation, relation_pred in zip(relations_per_sent, relations_pred_per_sent):
            relation_type, confidence_score = relation_pred
            if relation_type in required_relation_types and confidence_score > t:
                relation_tuple = (relation["subj"], relation["obj"])
                required_tuples.add(relation_tuple)
                if relation_tuple not in required_tuples_with_scores:
                    required_tuples_with_scores[relation_tuple] =  confidence_score
                else:
                    previous_value = required_tuples_with_scores[relation_tuple]
                    required_tuples_with_scores[relation_tuple] = max(previous_value, confidence_score)
        relation_preds.append(relation_pred_per_sent)

    return required_tuples, required_tuples_with_scores

def extraction_gpt3(gpt3_model, relations):

    relation_preds = []
    for relations_per_sent in relations:
        sent = relation_per_sent["tokens"]
        response = gpt3_model(
        model="text-davinci-003",
        prompt="",
        max_tokens=100,
        temperature=0.1,
        top_p=k,
        frequency_penalty=0,
        presence_penalty=0
    )
    response_text = response['choices'][0]['text']
    sleep(5)
    return response_text

def processUserInput():
    sys.argv.pop(0)
    extraction_method = sys.argv[0]
    api_key = sys.argv[1]
    engine_id = sys.argv[2]
    open_ai_key = sys.argv[3]
    r = int(sys.argv[4])
    t = float(sys.argv[5])
    q = sys.argv[6]
    k = int(sys.argv[7])
   
    return extraction_method, api_key, engine_id, open_ai_key, r, t, q, k

def main():
    
    spacy_model = spacy.load("en_core_web_lg")
    spanbert_model = SpanBERT("./pretrained_spanbert")
    
    spacy2bert = {"ORG": "ORGANIZATION", "PERSON": "PERSON", "GPE": "LOCATION", "LOC": "LOCATION"}
    bert2spacy = {"ORGANIZATION": "ORG", "PERSON": "PERSON", "LOCATION": "LOC", "CITY": "GPE", "COUNTRY": "GPE", "STATE_OR_PROVINCE": "GPE"}
    r2required_relations = {1: [("PERSON", "ORG")], 2: [("PERSON", "ORG")], 3: [("PERSON", "LOC"), ("PERSON", "GPE")], 4: [("ORG", "PERSON")]}
    r2required_entities = {1: ["PERSON", "ORG"], 2: ["PERSON", "ORG"], 3: ["PERSON", "LOC", "GPE"], 4: ["PERSON", "ORG"]}

    # openai settings
    openai.api_key = ""

    extraction_method, api_key, engine_id, openai_key, r, t, q, k = processUserInput()

    required_relation_types = r2required_relations[r]
    required_entity_types = r2required_entities[r]
    
    #step 1
    x = set()

    search_results = list()

    service = build(
        "customsearch", "v1", developerKey=api_key
    )

    while True:

        data = service.cse().list(q=" ".join(q), cx=engine_id,).execute()

        for item in data["items"]:
            url = item["link"]
            title = item["title"]
            description = item["snippet"]
            search_results.append((url,title,description))

        # this dictionary use url as the key and the text from website as the value
        plain_text_dict = {}
        used_queries = set()

        for result in search_results:
            curr_url = i[0]
            if curr_url not in plain_text_dict:
                webpage_text = get_text(i[0])
                if webpage_text != None:

                    sent2ents = process_text(spacy_model, webpage_text)
                    sent2ents_required = process_required_entities(sent2ents, required_entity_types)
                    pairs_required, sents_required = process_required_pairs(sent2ents_required, required_relation_types, spacy2bert)
                    unique_tuples, unique_tuples_with_scores = process_relations(model, pairs_required, sents_required, t)

                    if extraction_method == "spanbert":
                        unique_tuples_with_scores_ordered = sorted(unique_tuples_with_scores, key=lambda x:x[1], reverse=True)

                        if len(unique_tuples) > k:
                            return unique_tuples_with_scores_ordered[:k]
                        else:
                            for unique_tuple in unique_tuples_with_scores_ordered:
                                key, value = unique_tuple
                                if key in used_queries:
                                    continue
                                else:
                                    used_queries.add(key)
                                    q = key
                                    break
                    elif extraction_method == "gpt3":
                        if len(unique_tuples) > k:
                            return unique_tuples[:k]
                        else:
                            for unique_tuple in unique_tuples:
                                if unique_tuple in used_queries:
                                    continue
                                else:
                                    used_queries.add(unique_tuple)
                                    q = unique_tuple
                                    break
                    else:
                        raise NotImplementedError
        # for i in plain_text_dict:
        #     print(i)
        #     print(plain_text_dict)
        #     print("----------")

if __name__ == "__main__":
# python3 test.py -spanbert AIzaSyDm0Wcp0OqqLiWypz0ijCRMjkHZ2mYisJs 2d6a0e6f605702952 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 2 0.7 "bill gates microsoft" 10

    main()
