import requests
import json

API_KEY = "BdtMo6R8p47I80EOVgLdMDrGBHcltL2COPNF0BZc4sgvpx4UGImZ5c21VGR2bJ5V"
BASE_API_URL = "https://feature-requests.cloudpanel.io/api/v1/"

# sample URL to get the top most wanted features
# https://feature-requests.cloudpanel.io/api/v1/posts?view=most-wanted&limit=10&key=API_KEY

def get_top_10_features():
    url = f"https://feature-requests.cloudpanel.io/api/v1/posts?view=most-wanted&limit=10&key={API_KEY}"
    json_url = requests.get(url)
    data = json.loads(json_url.text)
    features = {}
    for d in data:
        print(d['id'], d['title'], d['votesCount'], d['user']['name'], f"https://feature-requests.cloudpanel.io/posts/{d['id']}/{d['slug']}")

get_top_10_features()
