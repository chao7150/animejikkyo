import requests
import profile
import json

def get(text, appid):
    baseurl = "http://jlp.yahooapis.jp/KeyphraseService/V1/extract"
    params = {
        'appid' : appid,
        'sentence' : text,
        'output' : 'json'
    }
    r = requests.get(baseurl, params = params)
    return json.loads(r.text)