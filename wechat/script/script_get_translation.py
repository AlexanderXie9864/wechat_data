#!/usr/bin/env python3
# coding=utf-8
# __author__: Alexander
import random
import hashlib
import urllib
import json
url_youdao = 'http://openapi.youdao.com/api'
dict = {}
dict['from'] = 'en'
dict['to'] = 'zh'
dict['appKey'] = '79c4754cb9bcb134'
dict['salt'] = random.randint(1000,3000)


def translateYoudao(text):
     global dict
     dict['q'] = text
     sign = dict['appKey'] + dict['q'] + str(dict['salt'])+'9sF5YA4TBuehuAEuO7UusQBcGSad3g9F'
     dict['sign'] = hashlib.md5(sign.encode()).hexdigest()
     data = urllib.parse.urlencode(dict).encode('utf-8')
     response = urllib.request.urlopen(url_youdao, data)
     content = response.read().decode('utf-8')
     data = json.loads(content)
     result = data['translation']
     return result

if __name__ == '__main__':
    print(translateYoudao('USA'))