__author__ = 'zhwang.kevin'

import json
import requests
from requests_toolbelt import MultipartEncoder

# payload = [{
#            'createUserID':10063,
#            'faceValue':100,
#            'rule':1,
#            'cardAmount':1
#            }]
# url = 'http://localhost:8080/travel/touristCard/add2CardTips'
# r = requests.post(url, json=payload)
# print(r.text)

data = {"userName":"wang","alias":"wode"}
data = [("alias","wode"),("alias","nide"),("userName","wangzhenghong"),("file",('area.json', open('file\\area.json', 'rb'), 'text/plain'))]
mData = MultipartEncoder(data)
url = 'http://localhost:8080/travel/user/test'
# requests.post(url, data=[('interests', 'football'), ('interests', 'basketball')])
r = requests.post(url, data=mData,headers={'Content-Type': mData.content_type})
print(r.text)
# url2 = 'http://localhost:8080/travel/touristCard/getCardTips?userID=10063'
# r = requests.get(url2)
# print(r.text)

