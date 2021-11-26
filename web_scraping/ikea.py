import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import pandas as pd
from urllib import request
import os
from tool import cleanup_content as clean

# if not os.path.exists("./cushions"):
#     os.mkdir("./cushions")

url = 'https://www.ikea.com.tw/zh/products/cushions-throws-and-chairpads/cushions'
headers = {"User-Agent":generate_user_agent()}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text,'html.parser')

productLists = soup.select('div[class="card px-0 px-md-4"]')
# productLists
for productList in productLists:
    itemsName = productList.select('h6')[0].text
    itemsType = clean(productList.select('h1')[0].text)
    itemsPrice = clean(productList.select('p')[0].text)
    # print(clean(itemsType))
    # print(clean(itemsPrice))
    itemUrl = 'https://www.ikea.com.tw/zh'+productList.a['href']
    print(itemsName.ljust(12,' '), itemsPrice.ljust(8,' '), itemsType, itemUrl)

    resItem = requests.get(itemUrl, headers=headers)
    soupItem = BeautifulSoup(resItem.text,'html.parser')
    imgs = ['https://www.ikea.com.tw'+i['href'] for i in soupItem.select('a[class="slideImg"]')]
    for idx, img in enumerate(imgs):
        print('\t', img)
        # img_path = './cushions/{}_{}.{}'.format(itemsName, idx, img.split(".")[-1])
        # request.urlretrieve(img, img_path)


