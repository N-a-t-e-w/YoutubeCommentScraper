import requests
import json
import re
import tkinter as tk

#########
#apiKey = ""
#########


def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        u"\u2019"
        u"\n"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

def getComments(apiKey, accountid, root, text):
    print("HELLO")
    # Channel to parse 
    # Us this to find ID https://commentpicker.com/youtube-channel-id.php
    #accountid = "UCDyrCJyFaOLc8OnnCd0Khcg"

    # Get 'uploads' playlist id
    response = requests.get("https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id="+ accountid + "&key="+apiKey)
    uploads = response.json()["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # Get playlist size 
    response = requests.get("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId="+uploads+"&key="+apiKey)
    numUploads = response.json()["pageInfo"]["totalResults"]

    # Get video ID
    response = requests.get("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=" + uploads + "&key=" +apiKey)

    videoIds = []

    print("Getting Video Ids")

    while(True):
        for i in range(0,len(response.json()["items"])):
            videoIds.append(response.json()["items"][i]["snippet"]["resourceId"]["videoId"])

        try:
            response = requests.get("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=" + uploads + "&key=" +apiKey +"&pageToken="+response.json()["nextPageToken"])
        except:
            break

    with open(accountid + "videoIds.json", "w+") as fout:
        json.dump(videoIds,fout)

    print("Done... Collecting comments")

    #Get comments
    comments = []
    counter = 0
    done = "0% Completed"


    for video in videoIds:
        done = str(counter/(len(videoIds)) * 100) + "% Completed"
        text.set(done)
        root.update()
        response = requests.get("https://www.googleapis.com/youtube/v3/commentThreads?key="+apiKey+"&textFormat=plainText&part=snippet&videoId=" + video + "&maxResults=100")
        while(True):
            for i in range(0,len(response.json()["items"])):
                comments.append(remove_emojis(response.json()["items"][i]["snippet"]["topLevelComment"]["snippet"]["textOriginal"]))
            try:
                print(done)
                response = requests.get("https://www.googleapis.com/youtube/v3/commentThreads?key="+apiKey+"&textFormat=plainText&part=snippet&videoId=" + video + "&maxResults=100&pageToken=" + response.json()["nextPageToken"])
            except:
                break      
        counter += 1


    print("Done... printing file")

    with open(accountid + "comments.json", "w+") as fout:
        json.dump(comments, fout)
        










