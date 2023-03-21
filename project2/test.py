from googleapiclient.discovery import build
import sys
import urllib.request 
from bs4 import BeautifulSoup

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
   
    return extraction_method,api_key,engine_id,open_ai_key,r,t,q,k

def main():
    
    extraction_method,api_key,engine_id,open_ai_key,r,t,q,k = processUserInput()
    #step 1
    x = set()

    searchResult = list()

    service = build(
        "customsearch", "v1", developerKey=api_key
    )
    data = service.cse().list(q=" ".join(q), cx=engine_id,).execute()

    for i in data["items"]:
        url = i["link"]
        title = i["title"]
        description = i["snippet"]
        searchResult.append((url,title,description))

    # this dictionary use url as the key and the text from website as the value
    plain_text_dict = {}
    for i in searchResult:
        curr_url = i[0]
        if curr_url not in plain_text_dict:
            webpage_text = get_text(i[0])
            if webpage_text != None:
                plain_text_dict[curr_url] = webpage_text
    # for i in plain_text_dict:
    #     print(i)
    #     print(plain_text_dict)
    #     print("----------")

if __name__ == "__main__":
# python3 test.py -spanbert AIzaSyDm0Wcp0OqqLiWypz0ijCRMjkHZ2mYisJs 2d6a0e6f605702952 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 2 0.7 "bill gates microsoft" 10

    main()
