import requests
# from bs4 import BeautifulSoup
import json
from user_agent import generate_user_agent
from urllib import request
import os
from random import randint
from time import sleep
from pymongo_connect import input_data_Tomongo as input

# if not os.path.exists('./trplus_footstools'):
#     os.mkdir('./trplus_footstools')

headers = {"User-Agent": generate_user_agent()}
# url = 'https://www.trplus.com.tw/TR_Furniture/c/EC_10090063'
tempurl = 'https://www.trplus.com.tw/l4/rest/product/list?categoryCode=EC_10090063&page=0&q=:relevance'
results = []

tempres = requests.get(tempurl, headers=headers)
tempdatas = json.loads(json.loads(tempres.text))
allpage = tempdatas['pages']['numberOfPages']
# print(allpage)
x=1
for i in range(0,allpage):
    url = 'https://www.trplus.com.tw/l4/rest/product/list?categoryCode=EC_10090063&page={}&q=:relevance'.format(i)
    res = requests.get(url, headers=headers)
    datas = json.loads(json.loads(res.text))
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
        itemDict.update({"brand":brand, "price":price, "imgurl":imgurl, "id":itemId, "url":itemUrl, "name":itemtitle, "origin_price":origin_price, "imagePath":imgpath})
        results.append(itemDict)
        print(x)
        x+=1
        sleep(randint(2,5))
    
    sleep(randint(1,5))

input('furniture', 'trplus', results)
    # print(results)
    # with open('./trplus_allpage.json', 'w', encoding='utf-8') as f:
    #     json.dump(results, f, ensure_ascii=False, indent=2)
