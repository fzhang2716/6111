import pprint
from googleapiclient.discovery import build
import sys

def processUserInput():
    sys.argv.pop(0)
    api_key = sys.argv[0]
    engine_id = sys.argv[1]
    percision_value = float(sys.argv[2])
    search_word = " ".join(sys.argv[3:])
    return api_key, engine_id,percision_value,search_word

def main():
    
    api_key, engine_id,percision_value,search_word = processUserInput()
    # print(api_key, engine_id,percision_value,search_word)
    searchResult = list()


    service = build(
        "customsearch", "v1", developerKey=api_key
    )
    
    data = service.cse().list(q=search_word, cx=engine_id,).execute()
    for i in data["items"]:
        url = i["formattedUrl"]
        title = i["title"]
        description = i["snippet"]
        searchResult.append((url,title,description))
       
    
    userfeedback = []
    for i in searchResult:
        url, title, description = i
        print((url,title,description))
        rel = input(" relevent? type Y/N ")
        if(rel == "Y" or rel == "y"):
            userfeedback.append(1)
        else:
            userfeedback.append(0)



if __name__ == "__main__":
# python3 test.py AIzaSyDm0Wcp0OqqLiWypz0ijCRMjkHZ2mYisJs 2d6a0e6f605702952 0.1 steve jobs

    main()
