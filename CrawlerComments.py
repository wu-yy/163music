# -*- coding:utf-8 -*-
import EncryptUtil
import json
import requests
import  chardet
import time
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf8')
def getUTF8(str):
    strEncode=chardet.detect(str)
    return str.decode(strEncode['encoding'])#.encode('utf8')

filename=u"安河桥.txt"
f=open(filename,'w') #保存评论的文件

class Crawler(object):

    def __init__(self,id):
        modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.nonce = '0CoJUm6Qyw8W8jud'
        pubKey = '010001'
        self.secKey = EncryptUtil.createSecretKey(16)
        #首先产生16位密钥，进行RSA加密
        self.encSecKey = EncryptUtil.rsaEncrypt(self.secKey, pubKey, modulus)
        self.musicId = id
        self.requestUrl = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_%d/" % int(id)
        self.headers = {
            'Host': 'music.163.com',
            'Connection': 'keep-alive',
            'Content-Length': '484',
            'Cache-Control': 'max-age=0',
            'Origin': 'http://music.163.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'DNT': '1',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'Cookie':'Province=010; City=010; UM_distinctid=1602578c1d752a-05caafbbb6b4ed-5d1b3316-100200-1602578c1d8125; __gads=ID=df9439195f8812f3:T=1512457091:S=ALNI_Mbq3NxhcJNKV34hJxpeRl1xHJu_uw; vjuids=-24b9e9c81.1602578f3da.0.916edb1478579; vjlast=1512457172.1512457172.30; _ntes_nnid=4a0115d9d11deb7f4f95440f93d3485a,1512457171947; _ntes_nuid=4a0115d9d11deb7f4f95440f93d3485a; vinfo_n_f_l_n3=f1e95f51a84140be.1.0.1512457171960.0.1512458909433; usertrack=ezq0pVoqLxBf/xF7BigcAg==; _ga=GA1.2.236401197.1512714080; JSESSIONID-WYYY=CRybQfpQKiFpF%5C4ZF8lT8FkR2UT5VzD%5CFrq6qHiRPF2F4VWg1IhmPANEX66b53GmxXTgmx3QMnTeOAV8izBujINqBwPfOXM6UXGnxOpFuqfMnYVz%5CY1NWI2%5CdeSyM0m6xMJcopgCypx4xc8Ms%2BcXqv1B2b%2FnyuT9yNFMI%2FdZZvFTvzB0%3A1513256859889; _iuqxldmzr_=32; MUSIC_U=bd0b51d45f62f43e874fa07a67c458f542429f515c9d39e6fb15c9d06b36f5219c5bb1743367c4acda7e02b06424f495de39c620ce8469a8; __remember_me=true; __csrf=ae2e25640544b05745ace01b09aae8f9; __utma=94650624.236401197.1512714080.1513253066.1513255628.3; __utmb=94650624.7.10.1513255628; __utmc=94650624; __utmz=94650624.1513255628.3.3.utmcsr=blog.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/wangjiawei0227/article/details/73431035'
        } #注意这里面的cookie 是从浏览器复制的，不要直接粘贴cookie代码，根据个人登录信息进行复制


    def getComment(self, offset):
            text = {
                'username': "",  #可以为空
                'password': "",  #可以为空
                'rememberLogin': 'true',
                'offset': offset
            }
            text = json.dumps(text)
            #进行两次AES加密
            encText = EncryptUtil.aesEncrypt(EncryptUtil.aesEncrypt(text, self.nonce), self.secKey)
            data = {
                'params': encText,
                'encSecKey': self.encSecKey
            }
            res = requests.post(self.requestUrl, headers=self.headers, data=urllib.urlencode(data))
            jsonData = res.json()
            self.databaseSave(jsonData)
            return int(jsonData["total"])

    def databaseSave(self, jsonData):
        if(jsonData!=None):
            for comment in jsonData["comments"]:
                commentData = {
                    'id': str(comment["commentId"]),
                    'user': str(comment["user"]["userId"]),
                    'content': (comment["content"]),
                    'likeCount': str(comment["likedCount"]),
                    'commentTime': str(EncryptUtil.timeStamp(comment["time"])),
                    'musicId': str(self.musicId)
                }
                userData = {
                    'id': str(comment["user"]["userId"]),
                    'username': comment["user"]["nickname"],
                    'avatarUrl': comment["user"]["avatarUrl"]
                }

                if not comment["beReplied"] == []:
                    commentData["reComment"] = str(comment["beReplied"][0]["user"]["userId"])

                #将评论写入文件
                f.write(comment['content']+'\n')


    def process(self, offset):
        if offset == -1:
            return
        off = offset
        total = self.getComment(off)
        print('评论的总数：',total)
        while off < total:
            off += 10
            self.getComment(off)

def main(id):
    c = Crawler(id)
    c.process(1)

if __name__ == '__main__':
    main(66842)
    f.close()