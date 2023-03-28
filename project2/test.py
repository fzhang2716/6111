from googleapiclient.discovery import build
import sys
import urllib.request 
from bs4 import BeautifulSoup
import spacy
from spanbert import SpanBERT
import itertools
import openai
from tqdm import tqdm

def get_text(url, idx, length, extraction_method):

    with open("transcript{}.txt".format(extraction_method), "a") as output_file:
        output_file.write("URL ( {} / {}): {}\n".format(idx+1,length,url))
        output_file.write("        Fetching text from url ...\n")
    
    text = ""
    try:
        html = urllib.request.urlopen(url)
        htmlParse = BeautifulSoup(html, 'html.parser')
    except urllib.error.HTTPError: 
        return None
    for para in htmlParse.find_all("p"):
        text = text + para.get_text()
    if len(text) == 0:
        with open("transcript{}.txt".format(extraction_method), "a") as output_file:
            output_file.write("        Fail to fetch the text.\n")
        return None
    if len(text)>10000:
        with open("transcript{}.txt".format(extraction_method), "a") as output_file:
            output_file.write("        Trimming webpage content from {} to 10000 characters\n".format(len(text)))
        text = text[ 0 : 10000 ]
    
    with open("transcript{}.txt".format(extraction_method), "a") as output_file:
        output_file.write("        Webpage length (num characters): {}\n".format(len(text)))
        output_file.write("        Annotating the webpage using spacy...\n")

    return text

def process_text(model, text):

    sentence2entities = []

    processed_text = model(text)
    for sent in processed_text.sents:
        named_entities_per_sent = sent.ents
        sentence2entities.append({"sentence": sent, "named_entities": named_entities_per_sent})

    return sentence2entities

def process_required_entities(sent2ents, required_entity_types):

    sent2ents_processed = []

    for ents_per_sent in tqdm(sent2ents):
        sent, named_entities_per_sent = ents_per_sent["sentence"], ents_per_sent["named_entities"]
        required_named_entities = [ent for ent in named_entities_per_sent if ent.label_ in required_entity_types]
        if len(required_named_entities) != 0:
            sent2ents_processed.append({"sentence": sent, "named_entities": named_entities_per_sent})

    return sent2ents_processed

def process_required_pairs(sent2ents, required_relation_types, spacy2bert):

    required_pairs, required_sents = [], []

    for ents_per_sent in tqdm(sent2ents):

        sent, named_entities_per_sent = ents_per_sent["sentence"], ents_per_sent["named_entities"]

        required_ents = {}
        pairs_per_sent = []

        for ent in named_entities_per_sent:
            name, label = ent.text, ent.label_
            if label not in required_ents:
                required_ents[label] = []
            required_ents[label].append(ent)

        for relation_type in required_relation_types:
            subj, obj = relation_type
            if subj not in required_ents or obj not in required_ents:
                continue
            subj_ents, obj_ents = required_ents[subj], required_ents[obj]
            relation_indexs = [(i, j) for i in range(len(subj_ents)) for j in range(len(obj_ents))]
            for idx in relation_indexs:
                subj_ent, obj_ent = subj_ents[idx[0]], obj_ents[idx[1]]
                subj_info = (subj_ent.text, spacy2bert[subj_ent.label_], (subj_ent.start, subj_ent.end-1))
                obj_info = (obj_ent.text, spacy2bert[obj_ent.label_], (obj_ent.start, obj_ent.end-1))
                tokens = [token.text for token in sent]
                pairs_per_sent.append({"tokens": tokens, "subj": subj_info, "obj": obj_info})

        if len(pairs_per_sent) != 0:
            required_pairs.append(pairs_per_sent)
            required_sents.append(sent)
    
    return required_pairs, required_sents

def process_relations(model, pairs, sents, confidence_threshold, required_relation_types_spanbert, required_relation_types, X, X_with_scores):
    if isinstance(model, SpanBERT):
        return extraction_spanbert(model, pairs, confidence_threshold, required_relation_types_spanbert, X, X_with_scores)
    elif isinstance(model, 'method'):
        return extraction_gpt3(model, sents, required_relation_types, X)
    else:
        raise NotImplementedError

def extraction_spanbert(spanbert_model, relations, t, required_relation_types, required_tuples, required_tuples_with_scores):


    num_extracted_relations = 0
    num_annotated_sentences = 0

    for sent_idx, relations_per_sent in enumerate(tqdm(relations)):
        relations_pred_per_sent = spanbert_model.predict(relations_per_sent)

        if sent_idx % 5 == 0 and sent_idx > 0:
            with open("transcript-spanbert.txt", "a") as output_file:
                output_file.write("Processed {}/{} sentences.\n".format(sent_idx, len(relations)))
        
        isAnnotated = False

        for relation, relation_pred in zip(relations_per_sent, relations_pred_per_sent):

            relation_type, confidence_score = relation_pred

            if relation_type in required_relation_types and confidence_score > t:

                num_extracted_relations += 1
                isAnnotated = True

                with open("transcript-spanbert.txt", "a") as output_file:
                    output_file.write("=== Extracted Relation ===\n")
                with open("transcript-spanbert.txt", "a") as output_file:
                    output_file.write("Input Tokens:{}\n".format(relation["tokens"]))

                relation_tuple = (relation["subj"][0], relation_type, relation["obj"][0])
                # relation_tuple = (relation["subj"], relation["obj"])
                required_tuples.add(relation_tuple)

                with open("transcript-spanbert.txt", "a") as output_file:
                    output_file.write("Output Confidence:{};\t Subject:{};\t Object:{}\t \n".format(confidence_score, relation["subj"][0], relation["obj"][0]))
                with open("transcript-spanbert.txt", "a") as output_file:
                    output_file.write("Adding to set of extracted relations\n")
                    output_file.write("===============================\n")

                if relation_tuple not in required_tuples_with_scores:
                    required_tuples_with_scores[relation_tuple] =  confidence_score
                else:
                    previous_value = required_tuples_with_scores[relation_tuple]
                    required_tuples_with_scores[relation_tuple] = max(previous_value, confidence_score)

        if isAnnotated:
            num_annotated_sentences += 1

    with open("transcript-spanbert.txt", "a") as output_file:
        output_file.write("Extracted annotations for  {}  out of total  {}  sentences\n".format(num_annotated_sentences, len(relations)))
        output_file.write("Relations extracted from this website: {} (Overall: {})\n".format(num_extracted_relations, len(required_tuples)))

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
        relation_preds.append(response_text)
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
    r2relation_types_printed = {1: "Schools_Attended", 2: "Work_For", 3: "Live_In", 4: "Top_Member_Employees"}
    r2relation_types = {1: "per:schools_attended", 2: "per:employee_of", 3: "per:cities_of_residence", 4: "org:top_members/employees"}

    # settings

    extraction_method, api_key, engine_id, openai_key, r, t, q, k = processUserInput()

    openai.api_key = openai_key
    
    required_relation_types = r2required_relations[r]
    required_entity_types = r2required_entities[r]
    required_spanbert_relations = r2relation_types[r]

    model = spanbert_model if extraction_method == "-spanbert" else openai.Completion.create
    
    service = build(
        "customsearch", "v1", developerKey=api_key
    )

    used_queries, used_urls = set(), set()
    X, X_with_scores = set(), {}

    # write configurations
    with open("transcript{}.txt".format(extraction_method), "w") as output_file:
        output_file.write("Parameters:"+"\n")
        output_file.write("Client key =\t {}\n".format(api_key))
        output_file.write("Engine key =\t {}\n".format(engine_id))
        output_file.write("OpenAI key =\t {}\n".format(openai_key))
        output_file.write("Method =\t {}\n".format(extraction_method))
        output_file.write("Relation =\t {}\n".format(r2relation_types_printed[r]))
        output_file.write("Threshold = \t {}\n".format(t))
        output_file.write("Query = \t {}\n".format(q))
        output_file.write("Loading necessary libraries; This should take a minute or so ...)")

    iter_idx = 0
    while True:

        with open("transcript{}.txt".format(extraction_method), "a") as output_file: 
            output_file.write("=========== Iteration: {} - Query: {} ===========".format(iter_idx, q) + "\n")

        iter_idx += 1

        search_results = []
        data = service.cse().list(q=q, cx=engine_id,).execute()

        for item in data["items"]:
            url = item["link"]
            title = item["title"]
            description = item["snippet"]
            search_results.append((url,title,description))

        for result_idx, result in enumerate(search_results):
            curr_url = result[0]
            print("URL {} processing:".format(result_idx))

            if curr_url not in used_urls:
                used_urls.add(curr_url)
                webpage_text = get_text(result[0], result_idx, len(search_results), extraction_method)

                if webpage_text != None:
                    with open("transcript{}.txt".format(extraction_method), "a") as output_file:
                        output_file.write("Annotating the webpage using spacy...\n")
                    sent2ents = process_text(spacy_model, webpage_text)
                    with open("transcript{}.txt".format(extraction_method), "a") as output_file:
                        output_file.write("Extracted {} sentences. Processing each sentence one by one to check for presence of right pair of named entity types; if so, will run the second pipeline ...\n".format(len(sent2ents)))

                    print("processing entities for url {}...".format(result_idx))
                    sent2ents_required = process_required_entities(sent2ents, required_entity_types)
                    print("processing entities pairs for url {}...".format(result_idx))
                    pairs_required, sents_required = process_required_pairs(sent2ents_required, required_relation_types, spacy2bert)
                    print("processing relation extraction for url {}...".format(result_idx))
                    X, X_with_scores = process_relations(model, pairs_required, sents_required, t, required_spanbert_relations, required_relation_types, X, X_with_scores)
                else:
                    print("webpage contains nothing.")
    
        if extraction_method == "-spanbert":
            X_with_scores_ordered = sorted(X_with_scores.items(), key=lambda x:x[1], reverse=True)
            assert len(X) == len(X_with_scores)

            if len(X) > k:
                results = X_with_scores_ordered[:k]
                with open("transcript{}.txt".format(extraction_method), "a") as output_file:
                    output_file.write("================== ALL RELATIONS for {} ( {} ) =================\n".format(r2relation_types[r], k))
                    for result in results:
                        relations, confidence_score = result
                        print(relations, confidence_score)
                        output_file.write("Confidence:{}\t Subject:{}\t Object:{}\n".format(confidence_score, relations[0], relations[2]))
                    output_file.write("Total # of iterations = {}\n".format(iter_idx))
                return
            else:
                for unique_tuple in X_with_scores_ordered:
                    relation_tuple, confidence_score = unique_tuple
                    query = (relation_tuple[0], relation_tuple[2])
                    if query in used_queries:
                        continue
                    else:
                        used_queries.add(query)
                        q = query
                        break

        elif extraction_method == "-gpt3":
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



if __name__ == "__main__":
# python3 test.py -spanbert AIzaSyDm0Wcp0OqqLiWypz0ijCRMjkHZ2mYisJs 2d6a0e6f605702952 replace-with-openai-key-here 2 0.7 "bill gates microsoft" 10

    main()

    # spacy_model = spacy.load("en_core_web_lg")
    # spanbert_model = SpanBERT("./pretrained_spanbert")
    
    # spacy2bert = {"ORG": "ORGANIZATION", "PERSON": "PERSON", "GPE": "LOCATION", "LOC": "LOCATION"}
    # bert2spacy = {"ORGANIZATION": "ORG", "PERSON": "PERSON", "LOCATION": "LOC", "CITY": "GPE", "COUNTRY": "GPE", "STATE_OR_PROVINCE": "GPE"}
    # r2required_relations = {1: [("PERSON", "ORG")], 2: [("PERSON", "ORG")], 3: [("PERSON", "LOC"), ("PERSON", "GPE")], 4: [("ORG", "PERSON")]}
    # r2required_entities = {1: ["PERSON", "ORG"], 2: ["PERSON", "ORG"], 3: ["PERSON", "LOC", "GPE"], 4: ["PERSON", "ORG"]}
    # r2relation_types = {1: "per:schools_attended", 2: "per:employee_of", 3: "per:cities_of_residence", 4: "org:top_members/employees"}
    # # openai settings

    # extraction_method, api_key, engine_id, openai_key, r, t, q, k = processUserInput()

    # openai.api_key = openai_key
    
    # required_relation_types = r2required_relations[r]
    # required_entity_types = r2required_entities[r]
    # required_spanbert_relations = r2relation_types[r]

    # model = spanbert_model if extraction_method == "-spanbert" else openai.Completion.create

    # webpage_text = "Bill Gates stepped down as chairman of Microsoft in February 2014 and assumed a new post as technology adviser to support the newly appointed CEO Satya Nadella."
    
    # sent2ents = process_text(spacy_model, webpage_text)
    # sent2ents_required = process_required_entities(sent2ents, required_entity_types)
    # pairs_required, sents_required = process_required_pairs(sent2ents_required, required_relation_types, spacy2bert)
    # unique_tuples, unique_tuples_with_scores = process_relations(model, pairs_required, sents_required, t, required_spanbert_relations)
    # print(unique_tuples)



