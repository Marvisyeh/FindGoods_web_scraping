import requests
from urllib import request
from user_agent import generate_user_agent
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import json,os,pprint
from tool import cleanup_content as clean
from pymongo_connect import input_data_Tomongo as in_mongo
from pymongo_connect import url_set

## product_insidePage
def inside(itemUrl,itemName):
    
    headers = {"User-Agent":generate_user_agent()}
    resItem = requests.get(itemUrl, headers=headers)
    soupItem = BeautifulSoup(resItem.text,'html.parser')
    
    content = json.loads(soupItem.select('input[name="productInfo"]')[0]['value']) #itemID json
    title = soupItem.select('div[class="itemInfo mt-4"]')
    cn_title = (title[0].h1.text)
    content['cn_title']=cn_title
    # print(title[0].select('p[class="partNumber"]')[1].text)
    # print(type(content))
    itemId = content['id'] #產品ID(檢查重複用)
    itemdes = soupItem.select('div[class="tab-pane fade active show"]') #item describe
    itemdes_key = itemdes[0].select('h3')[0].text #itemdesKey
    itemdes_values = [i.text for i in itemdes[0].select('p')]
    content[itemdes_key]=itemdes_values
    itemInfo= {(tr.text.strip('\n')).split(':')[0]:(tr.text.strip('\n')).split(':')[1] for tr in itemdes[0].select('table')[0].select('tr')}
    # table1 = [i.text for i in soupItem.select('table')[0].select('td')]
    content['size']=itemInfo
    # print(itemdes_key,itemdes_values,itemInfo)
    imgs = ['https://www.ikea.com.tw'+i['href'] for i in soupItem.select('a[class="slideImg"]')]
    content['imgurl']=imgs
    shop = imgs[0].split('.')[1]
    if not os.path.exists('./{}'.format(shop)):
        os.mkdir('./{}'.format(shop))
    if not os.path.exists('./{}/{}'.format(shop,itemName)):
        os.mkdir('./{}/{}'.format(shop,itemName))
    img_path_list=[]
    for idx, img in enumerate(imgs):
        print('\t', img)
        # downloadImg
        img_path = './{}/{}/{}_{}_{}.{}'.format(shop,itemName,shop[0:2],itemId, idx, img.split(".")[-1])
        img_path_list.append(img_path)
        request.urlretrieve(img, img_path)
    content['image_path']=img_path_list
    # print(content)

    return itemId,content

## comment and star
def comments(itemId):
    firsturl = 'https://display.powerreviews.com/m/43967/l/zh_TW/product/{}/reviews?apikey=1e9ad068-6739-4743-921c-7433b46b48ff&_noconfig=true'.format(itemId)
    print(firsturl)
    headers = {'User-Agent': generate_user_agent()}
    firstres = requests.get(firsturl, headers=headers)
    firstJson = json.loads(firstres.text)
    # print(firstJson)
    try:
        total_results = firstJson["paging"]["total_results"] #評論數
    # print(total_results)
    except:
        print(firstJson)
        total_results = 0
    if total_results == 0:
        wraper = {}
        wraper['id']=itemId
        wraper['total_results']=total_results
        wraper['total_reviews']=0.0
        wraper['star']=''
        return wraper
    else:
        total_reviews=(firstJson['results'][0]['rollup']['average_rating']) #總評論分數
        wraper = {}
        wraper['id']=itemId
        wraper['total_results']=total_results
        wraper['total_reviews']=total_reviews
        com_num=1
        # print(wraper)
        commdic = {} #將每則評論寫入字典
        for i in range(0,total_results, 25):
            # print(i)
            itemid = int(itemId)
            page = i
            url = 'https://display.powerreviews.com/m/43967/l/zh_TW/product/{}/reviews?paging.from={}&paging.size=25&_noconfig=true&apikey=1e9ad068-6739-4743-921c-7433b46b48ff'.format(itemid, page)
            
            res = requests.get(url, headers=headers)
            comm = json.loads(res.text)
            # print(comm)
            try:
                for contents in comm['results'][0]['reviews']: #取出所有reviews
                    # print(contents)

                    every_reviews = {i['label']:i['value'][0] for i in contents['details']['properties'][-4:]} #每個人的評分分數
                    # print({i['label']:i['value'][0] for i in contents['details']['properties'][-4:]}) 
                    try:
                        rec_friends = contents['details']['bottom_line'] #是否推薦給朋友
                        every_reviews['rec_friends']=rec_friends
                        # print(contents['details']['bottom_line'])
                    except KeyError as e:
                        rec_friends = ''
                        every_reviews['rec_friends']=rec_friends
                        # print('')
                    useful = contents['metrics']#是否有用，個別總評分
                    every_reviews.update(useful)
                    # print(contents['metrics']) 
                    
                    headline = contents['details']['headline'] #評論title
                    sub = contents['details']['comments'].replace('\n',' ') #內容
                    every_reviews['description']=headline+' '+sub
                    # print(headline, sub)
                    # print(every_reviews)

                    commdic[f'comment{com_num}']= every_reviews
                    com_num+=1
                # pprint.pprint(dic)
                sleep(randint(1,2))
            except:
                print(firstJson)
                every_reviews = firstJson

        wraper['star']=commdic
        # pprint.pprint(wraper)
        return wraper


# 所有商品
def ikea_pro(collection,category,itemName):
    # url = 'https://www.ikea.com.tw/zh/products/sofas/footstools'
    url = 'https://www.ikea.com.tw/zh/products/{}/{}'.format(category,itemName)
    headers = {"User-Agent":generate_user_agent()}
    # listPage
    id = 1
    # results_list = []
    idset=set()
    while True:
        print(url)

        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text,'html.parser')
        
        productLists = soup.select('div[class="card px-0 px-md-4"]')
        # print(productLists)
        for productList in productLists:
            item={}
            itemsName = productList.select('h6')[0].text
            itemsType = (productList.select('h1')[0].text)
            itemsPrice = clean(productList.select('p')[0].text)
            # print(clean(itemsType))
            # print(clean(itemsPrice))
            itemUrl = 'https://www.ikea.com.tw/zh'+productList.a['href']
            print(itemsName.ljust(12,' '), itemsPrice.ljust(8,' '), itemsType, itemUrl)
            item['_id']=id
            item['CNname'] = itemsName
            item['url'] = itemUrl
            try:
                itemId,content = inside(itemUrl,itemName)
            except Exception as e:
                print(e)
                continue
            
            if itemId in idset:
                print(f'{itemId} is already in datas')
                pass
            else:
                idset.add(itemId)
                itemreviews = comments(itemId)
                content.update(itemreviews)
                item.update(content)
                # results_list.append(item)
                idx,exists_url = url_set('ikea2',collection)
                if itemUrl in exists_url:
                    print('item already in database')
                else:
                    item['_id']=idx
                    in_mongo('ikea2',collection,item)
                    print(id)
            print(item)
            id+=1
            sleep(randint(1,4))

        try:
            url = soup.select('a[class="page-link"][data-sitemap-url]')[0]['data-sitemap-url']
            sleep(randint(2,5))
        except IndexError as e:
            print(e)
            break

if __name__ == '__main__':
    # final_ver
    # ikea_pro('sofas','footstools')
    # ikea_pro('cushions-throws-and-chairpads','cushions')



    #02_insideTest
    # url = 'https://www.ikea.com.tw/zh/products/armchairs-footstool-and-sofa-tables/footstools/bosnas-art-20266683'
    # itemId,content = inside(url,url.split('/')[-2])
    
    
    # #03 commentsTest
    # itemId = '20266683'
    # result = comments(itemId)

#     content.update(result)
#     print(content)
# 
    items = {'footstool':['sofas','footstools'],'frame':['home-decoration','frames-and-wall-decoration'],'vasesbowl':['home-decoration','vases-bowls-and-accessories'],'mugs':['tableware','coffee-and-tea-accessories'],'lamps':['luminaires','table-lamps'],'desk':['work-desks','home-desks'],'Cushion':['cushions-throws-and-chairpads','cushions']}
    # items = {'Cushion':['cushions-throws-and-chairpads','cushions']}
    
    for collection,j in items.items():
        ikea_pro(collection,j[0],j[1])