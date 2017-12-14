#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import os
import base64
from Crypto.Cipher import AES
from pprint import pprint


def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext


def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = int(text.encode('hex'), 16)**int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)


def createSecretKey(size):
    return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]


url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_30953009/?csrf_token='
headers = {
    'Cookie': 'Province=010; City=010; UM_distinctid=1602578c1d752a-05caafbbb6b4ed-5d1b3316-100200-1602578c1d8125; __gads=ID=df9439195f8812f3:T=1512457091:S=ALNI_Mbq3NxhcJNKV34hJxpeRl1xHJu_uw; vjuids=-24b9e9c81.1602578f3da.0.916edb1478579; vjlast=1512457172.1512457172.30; _ntes_nnid=4a0115d9d11deb7f4f95440f93d3485a,1512457171947; _ntes_nuid=4a0115d9d11deb7f4f95440f93d3485a; vinfo_n_f_l_n3=f1e95f51a84140be.1.0.1512457171960.0.1512458909433; usertrack=ezq0pVoqLxBf/xF7BigcAg==; _ga=GA1.2.236401197.1512714080; JSESSIONID-WYYY=yYIfCqtyMfOqg%5CiyhSdIPKSc6%2FBenqiyQGt6bHmZGhq3tnpfYuUB7mhlgbb%2B9ZSZwij4Q4OyAUWGu5Enk%2BeEUbAaoki9pdte9VwAyYOAzWSN6Pjcp7lHDQd2lqfezE6NuFM0767SStBIo%2FGBd6YV7%5CpNYoO41D4fy7Ewm42s7nGk%2B4s1%3A1513258829262; _iuqxldmzr_=32; MUSIC_U=bd0b51d45f62f43e874fa07a67c458f5778f2cb6a95d16c5c0dabf6ab682f0aa01d61cee838c1c69f6f7b7712ec0c786a70b41177f9edcea; __remember_me=true; __csrf=0cbff8510c2df15338e0363d276ea09f; __utma=94650624.236401197.1512714080.1513253066.1513255628.3; __utmb=94650624.15.10.1513255628; __utmc=94650624; __utmz=94650624.1513255628.3.3.utmcsr=blog.csdn.net|utmccn=(referral)|utmcmd=referral|utmcct=/wangjiawei0227/article/details/73431035',
    'Referer': 'http://music.163.com/'
}
text = {
    'username': '2384172887@qq.com',
    'password': '1155435642',
    'rememberLogin': 'true'
}
modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
nonce = '0CoJUm6Qyw8W8jud'
pubKey = '010001'
text = json.dumps(text)
secKey = createSecretKey(16)
encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
encSecKey = rsaEncrypt(secKey, pubKey, modulus)
data = {
    'params': encText,
    'encSecKey': encSecKey
}

req = requests.post(url, headers=headers, data=data)
pprint(req.json())
for content in req.json()['comments']:
    print content['content'].encode('utf-8')
    print
print req.json()['total']