import pprint
from googleapiclient.discovery import build
import sys

def processUserInput():
    sys.argv.pop(0)
    percision_value = float(sys.argv[-1])
    sys.argv.pop(-1)
    search_word = " ".join(sys.argv)
    return percision_value, search_word

def main():
    
    percision_value, search_word = processUserInput()
    searchResult = list()


    service = build(
        "customsearch", "v1", developerKey="AIzaSyDm0Wcp0OqqLiWypz0ijCRMjkHZ2mYisJs"
    )
    
    data = service.cse().list(q=search_word, cx='2d6a0e6f605702952',).execute()
    for i in data["items"]:
        url = i["formattedUrl"]
        title = i["title"]
        description = i["snippet"]
        searchResult.append((url,title,description))
       
    for i in searchResult:
        print(i)
    print(len(searchResult))
    # print(searchResult)

    


if __name__ == "__main__":
    main()
