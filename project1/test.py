import pprint
from googleapiclient.discovery import build
from keybert import KeyBERT
import sys
from copy import deepcopy

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
        
        twograms_keywords = keybert_model.extract_keywords(content, keyphrase_ngram_range=(2,2), stop_words='english')
        onegram_keywords = keybert_model.extract_keywords(content, keyphrase_ngram_range=(1,1), stop_words='english')
        return twograms_keywords, onegram_keywords
        
    for content in contents:
        twograms_keywords, onegram_keywords = get_keybert_score(content)
        occurred_words = set()
        for item in twograms_keywords:
            key, score = item
            if key not in query_dict:
                query_dict[key] = {}
                query_dict[key]["importance"] = 0.
                query_dict[key]["occurrence"] = 0
            word_1, word_2 = key.split()
            if word_1 not in query_dict:
                query_dict[word_1] = {}
                query_dict[word_1]["importance"] = 0.
                query_dict[word_1]["occurrence"] = 0
            if word_2 not in query_dict:
                query_dict[word_2] = {}
                query_dict[word_2]["importance"] = 0.
                query_dict[word_2]["occurrence"] = 0
                
            query_dict[key]["importance"] += score
            query_dict[word_1]["importance"] += score
            query_dict[word_2]["importance"] += score

            occurred_words.add(key)
            occurred_words.add(word_1)
            occurred_words.add(word_2)
            
        for item in onegram_keywords:
            key, score = item
            if key not in query_dict:
                query_dict[key] = {}
                query_dict[key]["importance"] = 0.
                query_dict[key]["occurrence"] = 0
            query_dict[key]["importance"] += score
            query_dict[key]["occurrence"] += 1
            
            occurred_words.add(key)
        
    for key in occurred_words:
        query_dict[key]["occurrence"] += 1
    
    return query_dict

def fetch_new_words(_query_dict, _search_words):
    
    previous_search_words = deepcopy(_search_words)
    new_word_count = 0
    word_lst = sorted(_query_dict.items(), key=lambda x: float(0.25 * x[1]["importance"]+0.75*x[1]["occurrence"]), reverse=True)
    
    for item in word_lst:
        word, score = item
        if word in _search_words:
            continue
        else:
            if len(word.split()) == 1:
                _search_words.append(word)
                new_word_count += 1
            else:
                word_1, word_2 = word.split()
                print(new_word_count)
                _search_words.append(word_1)
                new_word_count += 1
                if new_word_count >= 2:
                    break
                else:
                    _search_words.append(word_2)
                    new_word_count += 1
                    
        if new_word_count >= 2:
            break
    
    return _search_words

def reorder_new_words(query_dict, search_words):
    
    new_words = {}
    for word in search_words:
        try:
            new_words[word] = float(0.25 * query_dict[word]["importance"]+ 0.75 * query_dict[word]["occurrence"])
        except:
            new_words[word] = 0.

    new_words_reordered = sorted(new_words.items(), key=lambda x: x[1], reverse=True)
    
    return [word[0] for word in new_words_reordered]

def main():
    
    api_key, engine_id, target_precision, search_words = processUserInput()
    # print(api_key, engine_id,precision_value,search_word)


    service = build(
        "customsearch", "v1", developerKey=api_key
    )
    
    precision = 0
    query_dict = {}
    
    search_words = search_words.split()
    
    iteration = 0
    
    while precision < target_precision:
        
        with open("transcript.txt", "a") as output_file:
            output_file.write("=============== Iteration:{}=================".format(str(iteration))+"\n")
        
        searchResult = list()

        data = service.cse().list(q=" ".join(search_words), cx=engine_id,).execute()

        # retrieve search results
        for page_idx, page in enumerate(data["items"]):
            url = page["formattedUrl"]
            title = page["title"]
            description = page["snippet"].strip()
            full_text = title + ": " + description
            searchResult.append((url,title,description, full_text))

        if len(searchResult) < 10:
            print("please enter broad, ambiguous queries.")
            break
            
        # get user feedback
        user_feedback = []
        for result_idx, result in enumerate(searchResult):
            url, title, description, _ = result
            print(" ")
            print("result no.", result_idx+1)
            print(" url:", url)
            print(" title:", title)
            print(" description", description)
            rel = input(" relevant? type Y/N. ")
            ifRelevant = ""
            if rel in ["Y", "y"]:
                user_feedback.append(1)
                ifRelevant = "Yes"
            elif rel in ["N", "n"]:
                user_feedback.append(0)
                ifRelevant = "No"
            else:
                raise ValueError("Please type Y/N.")
            
            with open("transcript.txt", "a") as output_file:
                output_file.write(" "+"\n")
                output_file.write("result no."+ str(result_idx + 1) + "\n")
                output_file.write("relevant?:" + ifRelevant + "\n")
                output_file.write("[" + "\n")
                output_file.write("  url:" + url + "\n")
                output_file.write("  title:" + title + "\n")
                output_file.write("  description:" +  description + "\n")
                output_file.write("]" + "\n")     

        if sum(user_feedback)/ 10. >= target_precision:
            print("reach target precision at iter:{} with precision {}/{}.".format(iteration, sum(user_feedback), "10"))
            break
        elif sum(user_feedback) == 0:
            print("zero precision at iter:{}.".format(iteration))
            break
        
        # requery
        relevant_pages = fetch_relevant_pages(user_feedback, searchResult)
        query_dict = compute_word_scores(query_dict, relevant_pages)
        search_words = fetch_new_words(query_dict, search_words)
        search_words = reorder_new_words(query_dict, search_words)
        
        print("iter:{}\t current precision:{}/10\t new search words:{}".format(iteration, sum(user_feedback), " ".join(search_words)))
        
        iteration += 1
            
            
    
if __name__ == "__main__":
# python3 test.py AIzaSyDm0Wcp0OqqLiWypz0ijCRMjkHZ2mYisJs 2d6a0e6f605702952 0.1 steve jobs

    main()
