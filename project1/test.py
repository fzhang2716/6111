import pprint
from googleapiclient.discovery import build
from keybert import KeyBERT
import sys
import spacy

ner_model = spacy.load('en_core_web_sm')
keybert_model = KeyBERT()

def processUserInput():
    sys.argv.pop(0)
    api_key = sys.argv[0]
    engine_id = sys.argv[1]
    precision_value = float(sys.argv[2])
    search_word = " ".join(sys.argv[3:])
    return api_key, engine_id,precision_value,search_word

def fetch_relevant_pages(user_feedback, pages):
    relevant_pages = [page[3] for (feedback, page) in zip(user_feedback, pages) if feedback==1]
    return relevant_pages

def compute_word_scores(query_dict, contents):

    def get_keybert_score(content):
        
        twograms_keywords = keybert_model.extract_keywords(content, keyphrase_ngram_range=(1,2), stop_words='english')
        onegram_keywords = keybert_model.extract_keywords(content, keyphrase_ngram_range=(1,1), stop_words='english')
        scores = twograms_keywords + onegram_keywords
        return scores
        
    for content in contents:
        scores = get_keybert_score(content)
        for item in scores:
            key, score = item
            if key not in query_dict:
                query_dict[key] = {}
                query_dict[key]["importance"] = 0.
                query_dict[key]["occurence"] = 0
            query_dict[key]["importance"] += score

    for item in query_dict.items():
        key, value = item
        query_dict[key]["occurence"] += 1
    
    return query_dict

def fetch_new_words(query_dict, search_words):
    
    new_word_count = 0
    word_lst = sorted(query_dict.items(), key=lambda x: float(x[1]["importance"]/x[1]["occurence"]), reverse=True)
    
    for item in word_lst:
        word, score = item
        if word in search_words:
            continue
        else:
            search_words.append(word)
            new_word_count += 1
            if new_word_count >= 2:
                break
    
    return search_words

def reorder_new_words(query_dict, search_words):
    
    new_words = {}
    for word in search_words:
        new_words[word] = float(query_dict[word]["importance"]/query_dict[word]["occurence"])
    new_words_reordered = sorted(new_words.items(), key=lambda x: x[1], reverse=True)
    
    return [word[0] for word in new_words_reordered]

def main():
    
    api_key, engine_id, target_precision, search_words = processUserInput()
    # print(api_key, engine_id,precision_value,search_word)
    searchResult = list()


    service = build(
        "customsearch", "v1", developerKey=api_key
    )
    
    precision = 0
    query_dict = {}
    
    search_words = search_words.split()

    while precision < target_precision:
        
        data = service.cse().list(q=" ".join(search_words), cx=engine_id,).execute()
        for i in data["items"]:
            url = i["formattedUrl"]
            title = i["title"]
            description = i["snippet"]
            full_text = title + ": " + description
            searchResult.append((url,title,description, full_text))

        user_feedback = []
        for i in searchResult:
            url, title, description, _ = i
            print((url,title,description))
            rel = input(" relevent? type Y/N ")
            if(rel == "Y" or rel == "y"):
                user_feedback.append(1)
            else:
                user_feedback.append(0)

            relevant_pages = fetch_relevant_pages(user_feedback, searchResult)
            query_dict = compute_word_scores(query_dict, relevant_pages)
            search_words = fetch_new_words(query_dict, search_words)
            search_words = reorder_new_words(query_dict, search_words)
            
            
        



if __name__ == "__main__":
# python3 test.py AIzaSyDm0Wcp0OqqLiWypz0ijCRMjkHZ2mYisJs 2d6a0e6f605702952 0.1 steve jobs

    main()
