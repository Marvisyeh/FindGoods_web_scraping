import requests
from urllib import request
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
from tool import cleanup_content as clean
import json,os
from time import sleep
from random import randint
from pymongo_connect import input_data_Tomongo,url_set
def insidetrp(url):

    headers = {"User-Agent": generate_user_agent()}

    itemsres = requests.get(url, headers=headers)
    soup = BeautifulSoup(itemsres.text, 'html.parser')
    
    theDict = {}
    reviews_num = clean(soup.select('div[class="info__rating"]')[0].span.text) #評論人數
    theDict['total_results']=reviews_num
    stars = len(soup.select('div[class="info__rating"]')[0].select('i[class="fa fa-fw fa-star active"]')) #評論星等
    theDict['total_reviews']=stars
    # print(reviews_num,stars)
    # print(stars)
    datas = soup.select('div[class="col-12 clearfix"]')
    # print(datas)
    category = [i.a.text for i in soup.select('li[class="breadcrumb-item"]')]
    theDict['category'] = category
    for data in datas:
        describe = data.select('li')[0].text
        theDict["describe"] = describe
        # print(describe)
        # print("="*10)
        itemInfo =[size.text for size in data.select('div[class="info__aspect"]')]
        itemInfo =clean(itemInfo)
        theDict["itemInfo"] = [item for item in itemInfo]
        # print(sizes)
        # print("="*10)
    return theDict

def trplus_scribe(itemsid,collection):
    headers = {"User-Agent": generate_user_agent()}
    # url = 'https://www.trplus.com.tw/TR_Furniture/c/EC_10090063'
    # tempurl = 'https://www.trplus.com.tw/l4/rest/product/list?categoryCode=EC_10090063&page=0&q=:relevance'
    tempurl = 'https://www.trplus.com.tw/l4/rest/product/list?categoryCode={}&page=0&q=:relevance'.format(itemsid)
    
    results = []


    tempres = requests.get(tempurl, headers=headers)
    tempdatas = json.loads(json.loads(tempres.text))
    allpage = tempdatas['pages']['numberOfPages']
    print(allpage)
    # x=1

    for i in range(0,allpage):
        url = 'https://www.trplus.com.tw/l4/rest/product/list?categoryCode={}&page={}&q=:relevance'.format(itemsid,i)
        res = requests.get(url, headers=headers)
        datas = json.loads(json.loads(res.text))
        idx,checkduplicate = url_set('trplus',collection)
        
        if idx > 100:
            break
        else:
            for data in datas['products']:
                # print(data)
                itemUrl = 'https://www.trplus.com.tw'+data['GDURL']
                idx,checkduplicate = url_set('trplus',collection)
                checkduplicate=[]
                if itemUrl in checkduplicate:
                    continue
                else:
                    itemDict = {"_id":idx}
                    itemId = data['GDID']
                    brand = data['channel']
                    price = data['GDPRC']
                    itemtitle = data['GDNM']
                    origin_price = data['GDCPRC']
                    imgurl = data['GDImages']
                    imgpath = []
                    filename = url.split('.')[1]
                    if not os.path.exists('./{}'.format(filename)):
                        os.mkdir('./{}'.format(filename))
                    if not os.path.exists('./{}/{}'.format(filename,collection)):
                        os.mkdir('./{}/{}'.format(filename,collection))
                    for idx, url in enumerate(imgurl):
                        imagePath = './{}/{}/{}_{}_{}.{}'.format(filename,collection,brand,itemId, idx, url.split('.')[-1])
                        imgpath.append(imagePath)
                        # request.urlretrieve(url, imagePath)
                    theDict = insidetrp(itemUrl)
                    itemDict.update({"brand":brand, "price":price, "imgurl":imgurl, "id":itemId, "url":itemUrl, "name":itemtitle, "origin_price":origin_price, "imagePath":imgpath})
                    itemDict.update(theDict)
                    print(itemDict)
                    input_data_Tomongo('trplus',collection,itemDict)
                    results.append(itemDict)
                    # print(itemtitle,itemUrl,imgurl)
                    # x+=1
                sleep(randint(2,5))

            sleep(randint(1,5))


if __name__ == "__main__":

    
    items = {'footstool':'EC_10090063','frame':'EC_10001288','vasesbowl':'EC_10001291','mugs':'EC_30089977','lamps':'EC_10092406','desk':'EC_10090054','Cushion':'EC_10000025'}
    for i,k in items.items():
        # print(i,k)
        trplus_scribe(k,i)
    # trplus_scribe('EC_10034015','lamps')