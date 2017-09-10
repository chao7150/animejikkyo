import profile
import tweepy
import feature
import re
from collections import Counter
import random
import datetime

class Jikkyo:

    def __init__(self):
        self.auth = tweepy.OAuthHandler(profile.CONSUMER_KEY, profile.CONSUMER_SECRET)
        self.auth.set_access_token(profile.ACCESS_TOKEN, profile.ACCESS_SECRET)
        self.api = tweepy.API(self.auth)
        #self.api.update_status(datetime.datetime.today())

    def getHashtag(self):
        samples = self.api.home_timeline(count = 10)
        tags = []
        for s in samples:
            for t in s.entities["hashtags"]:
                tags.append(t["text"])
        if len(tags) == 0:
            #print("no jikkyo")
            return
        counter = Counter(tags)
        self.commonTag = counter.most_common(1)[0]
        if self.commonTag[1] < 3:
            #print("few jikkyo")
            return
        else:
            self.getTweets(self.commonTag[0])
            
    def getTweets(self, tag):
        searchTag = '#' + tag
        jikkyos = self.api.search(searchTag + " -RT -@", count = 10)
        dic = {}
        for j in jikkyos:
            dic = self.merge_dict_add_values(dic, feature.get(self.filter(j.text), profile.YAHOO_APPID))
        counter = Counter(dic)
        self.postTweet(counter.most_common(5))

    def postTweet(self, words):
        wordNum = self.gaussInt()
        random.shuffle(words)
        text = ""
        for w in words[:wordNum - 1]:
            text = text + w[0]
        text = text + " #" + self.commonTag[0]
        self.api.update_status(text)
        #print("tweeted")

    def gaussInt(self):
        seed = random.gauss(2, 1)
        if seed < 0.5:
            wordNum = 1
        elif seed > 5.5:
            wordNum = 5
        else:
            wordNum = round(seed)
        return wordNum

    def filter(self, text):
        out = text
        for hashtag in re.findall(r'[#＃]([\w一-龠ぁ-んァ-ヴーａ-ｚ]+)', text):
            r = r'[#＃]%s' % hashtag
            out = re.sub(r, '', out)
        return re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)", "", out)

    def merge_dict_add_values(self, d1, d2):
        return dict(Counter(d1) + Counter(d2))

if __name__ == "__main__":
    jikkyo = Jikkyo()
    jikkyo.getHashtag()
