import collections
import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import json
import os
from time import sleep
from random import randint
from urllib import request
from pymongo import MongoClient
import pymongo

# 連線mongodb
connection = MongoClient(host='localhost', port=27017)
db = connection.HomeSet
collection = db['footstool_main']
# # 建立資料夾
# if not os.path.exists('./footstools'):
#     os.mkdir('./footstools')


# url = 'https://www.ikea.com.tw/zh/products/home-decoration/plant-pots'
url = 'https://www.ikea.com.tw/zh/products/sofas/footstools'
headers = {'User-Agent': generate_user_agent()}
resultJson = []
x=1

for i in range(1,4):#頁數
    # print(i)
    payload = {'page':i}
    res = requests.get(url, headers=headers, params = payload)
    print(res.url) ##當前爬取的網址
    soup = BeautifulSoup(res.text, 'lxml')
    soupArticle = soup.select('div[class="card px-0 px-md-4"]') #每一頁的HTML

    for article in soupArticle: #當頁每個商品
        articleUrl = 'https://www.ikea.com.tw'+article.a['href'] #每個商品網址
        # print(x, articleUrl)

        articleItem = article.h1.text.replace(" ",'') #商品標籤
        titleItem = article.select('a[class="itemName"]')[0].text.strip('\n').replace(" ",'') #商品品牌
        # print(titleItem.ljust(12,' '), articleItem.ljust(20," "), articleUrl)
        
        resItems = requests.get(articleUrl, headers = headers) #爬取內頁
        soupItems = BeautifulSoup(resItems.text, 'lxml')
        itemsInform = {"_id":x}  #設定資料表ID
        itemsInform.update(json.loads(soupItems.select('input[name="productInfo"]')[0]['value']))
        itemsInform['url'] = articleUrl
        itemsInform['產品尺寸'] = {tr.text.strip('\n').strip(' ').split(':')[0]:tr.text.strip('\n').strip(' ').split(':')[1] for tr in soupItems.select('table')[0].select('tr')}
        # resultJson.append(itemsInform)
        
        imgelist = []
        for idx, imgItem in enumerate(soupItems.select('a[class="slideImg"]')): #下載圖片
#             print('https://www.ikea.com.tw'+imgItem['href']) #大圖
            imageUrl = ('https://www.ikea.com.tw'+imgItem.select('img')[0]['src'])#小圖
            imagePath = './footstools/{}_{}.{}'.format(articleItem.replace('/',''), idx, imageUrl.split('.')[-1])
            imgelist.append(imagePath)
            # request.urlretrieve(imageUrl, imagePath)
            # print('\t',imageUrl)
        
        itemsInform['imgPath'] = imgelist
        resultJson.append(itemsInform)
        try: #存入資料庫
            result = collection.insert_one(itemsInform)        
            print("已新增",itemsInform)
        except Exception as err:
            print(err)
        x+=1
        sleep(randint(2,5))
        
    sleep(randint(2,5))
    print("="*20)
#存入JSON
with open('./json_footstools_01.json', 'w', encoding='utf8') as jsonfile:
    jsonfile.write(json.dumps(resultJson))
# # with open('./CN_footstools.json', 'w', encoding='utf8') as f:
# #     json.dump(json.dumps(resultJson), f)
# # print(resultJson)