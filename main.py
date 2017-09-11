import profile
import re
from collections import Counter
import random
import feature
import tweepy

class Jikkyo:

    def __init__(self):
        self.auth = tweepy.OAuthHandler(profile.CONSUMER_KEY, profile.CONSUMER_SECRET)
        self.auth.set_access_token(profile.ACCESS_TOKEN, profile.ACCESS_SECRET)
        self.api = tweepy.API(self.auth)

        self.commontag = None

    def gethashtag(self):
        samples = self.api.home_timeline(count=10)
        tags = []
        for sam in samples:
            for tag in sam.entities["hashtags"]:
                tags.append(tag["text"])
        if tags:
            return
        counter = Counter(tags)
        self.commontag = counter.most_common(1)[0]
        if self.commontag[1] < 3:
            print("few jikkyo")
            return
        else:
            self.gettweets(self.commontag[0])

    def gettweets(self, tag):
        searchtag = '#' + tag
        jikkyos = self.api.search(searchtag + " -RT -@", count=10)
        dic = {}
        for j in jikkyos:
            tmpdic = feature.get(self.filter(j.text), profile.YAHOO_APPID)
            dic = self.merge_dict_add_values(dic, tmpdic)
        counter = Counter(dic)
        self.posttweet(counter.most_common(5))

    def posttweet(self, words):
        wordnum = self.gaussint()
        random.shuffle(words)
        text = ""
        for wrd in words[:wordnum]:
            text = text + wrd[0]
        text = text + " #" + self.commontag[0]
        self.api.update_status(text)

    @staticmethod
    def gaussint():
        seed = random.gauss(2, 1)
        if seed < 0.5:
            wordnum = 1
        elif seed > 5.5:
            wordnum = 5
        else:
            wordnum = round(seed)
        return wordnum

    @staticmethod
    def filter(text):
        out = text
        for hashtag in re.findall(r'[#＃]([\w一-龠ぁ-んァ-ヴーａ-ｚ]+)', text):
            reg = r'[#＃]%s' % hashtag
            out = re.sub(reg, '', out)
        return re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)", "", out)

    @staticmethod
    def merge_dict_add_values(dic1, dic2):
        return dict(Counter(dic1) + Counter(dic2))

if __name__ == "__main__":
    jikkyo = Jikkyo()
    jikkyo.gethashtag()
