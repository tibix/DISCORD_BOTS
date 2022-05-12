import requests
import json

channel_id = 'UC2K_1ag15SEOErUIbm5AWxw'
API_KEY = 'AIzaSyDVOamyKOJK44PMGviUTKbzF8cDPwexjL4'


def get_top_10_videos():
    url =f"https://youtube.googleapis.com/youtube/v3/search?part=id&channelId={channel_id}&maxResults=10&order=rating&key={API_KEY}"
    json_url = requests.get(url)
    data = json.loads(json_url.text)
    video_ids = []
    try:
        data = data['items']
        for d in data:
            video_ids.append(d['id']['videoId'])
    except:
        print('Could not get top 10 videos!')
        video_ids = None
    
    return video_ids


def get_last_10_videos():
    url =f"https://youtube.googleapis.com/youtube/v3/search?channelId={channel_id}&maxResults=10&order=date&key={API_KEY}"
    json_url = requests.get(url)
    data = json.loads(json_url.text)
    video_ids = []
    try:
        data = data['items']
        for d in data:
            video_ids.append(d['id']['videoId'])
    except:
        print('Could not grab latest 10 videos!')
        video_ids = None
    
    return video_ids
 

def get_video_title(video):
    url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={video}&key={API_KEY}"
    json_url = requests.get(url)
    data = json.loads(json_url.text)
    title = data['items'][0]['snippet']['title']

    return title

def get_top_10_comments(video):
    url = f"https://youtube.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video}&key={API_KEY}"
    json_url = requests.get(url)
    data = json.loads(json_url.text)
    comments = data['items']
    comment_ids = []
    for c in comments:
        comment_ids.append(c['id'])
    return comment_ids

# get top ten comments for the channel
def get_top_10_channel_comments():
    url = f"https://youtube.googleapis.com/youtube/v3/commentThreads?part=snippet&channelId={channel_id}&maxResults=10&order=rating&key={API_KEY}"
    json_url = requests.get(url)
    data = json.loads(json_url.text)
    comments = data['items']
    comment_ids = []
    for c in comments:
        comment_ids.append(c['id'])
    return comment_ids