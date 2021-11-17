import requests
# from bs4 import BeautifulSoup
import json
from user_agent import generate_user_agent
from urllib import request
import os
from trplus_inside import append_des

if not os.path.exists('./trplus_footstools'):
    os.mkdir('./trplus_footstools')

headers = {"User-Agent": generate_user_agent()}
# url = 'https://www.trplus.com.tw/TR_Furniture/c/EC_10090063'
url = 'https://www.trplus.com.tw/l4/rest/product/list?categoryCode=EC_10090063&page=0&q=:relevance'
results = []

res = requests.get(url, headers=headers)
datas = json.loads(json.loads(res.text))
# print(datas['pages'])
x=1
for data in datas['products']:
    # print(data)
    itemDict = {"_id":x}
    brand = data['channel']
    price = data['GDPRC']
    itemId = data['GDID']
    itemUrl = 'https://www.trplus.com.tw'+data['GDURL']
    itemtitle = data['GDNM']
    origin_price = data['GDCPRC']
    imgurl = data['GDImages']
    imgpath = []
    for idx, url in enumerate(imgurl):
        imagePath = './trplus_footstools/{}_{}.{}'.format(itemtitle, idx, url.split('.')[-1])
        imgpath.append(imagePath)
        # request.urlretrieve(url, imagePath)
    theDict = append_des(itemUrl)
    itemDict.update({"brand":brand, "price":price, "imgurl":imgurl, "itemId":itemId, "itenUrl":itemUrl, "itemtitle":itemtitle, "origin_price":origin_price, "imagePath":imgpath})
    itemDict.update(theDict)
    results.append(itemDict)
    x+=1

# print(results)
with open('./trplus_onepage1.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
