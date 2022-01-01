from random import randint
import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import json,re
from time import sleep
from pymongo_connect import input_data_Tomongo
from tool import cleanup_content as clean
def plus_des(url):

    headers = {'User-Agent' : generate_user_agent()}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    name = soup.select('h1[class="title translate"]')[0].text
    price = soup.select('div[class="price-wrap"]')[0].text.split('NT$')[1]
    # print(price)
    imgUrl = ['https:'+i['src'].replace('80x80','800x0') for i in soup.select('div[class="photos-thumbs"]')[0].select('img')]

    # des = {i.select('dt')[0].text.strip('\n').strip(' ').strip('\n').strip('：'):i.select('dd')[0].text.strip('\n').strip(' ').strip('\n') for i in soup.select('div[class="m-product-list-item"]')}
    # del des['付款方式']

    des = {clean(i.select('dt')[0].text):clean(i.select('dd')[0].text) for i in soup.select('div[class="m-product-list-item"]')}
    # print(des)
    result = {}
    values = ('商品材質','商品產地','商品熱門度','商品摘要')
    for k,v in des.items():
        # print(k,':',v)
        if k in values:
            result[k]=v
    # print(result)

    # print(des)
    plus = {"name":name, "price":price, "imgurl":imgUrl, "others":result}
    return plus

def main_scrap():

    final = []
    url = 'https://www.pinkoi.com/browse?category=5&subcategory=543'
    for i in range(1,2):
        # print(url)
        headers = {'User-Agent' : generate_user_agent()}
        res = requests.get(url, headers = headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        cat = soup.select('head')[0].select('title')[0].contents
        cate = (re.sub('\W+',' ',cat[0]))

        inside_list = []
        # print(soup.select('script[type="application/ld+json"]'))
        for i in soup.select('script[type="application/ld+json"]'):
            # print(i.contents)
            for j in i.contents:
                # print(j)
                # print(j['name'])
                inside_list.append(json.loads(j))
        itemList=inside_list[1:]
        final.extend(itemList)
            
        path=inside_list[0]
        print(path)
        #取得下一頁url
        url = soup.select('link[rel="next"]')[0]['href']
        sleep(randint(1,4))
    # print(final)


    # name_1 = [n['name'] for n in [p['item'] for p in path['itemListElement']]]
    # thename = '_'.join(name_1)

    results = []
    for idx,i in enumerate(final):
    #     print(idx,i)
        url = i['offers']['url']
        adddes = plus_des(url)
        itemDic={}
        itemDic['_id']=idx+1
        itemDic.update(i)
        itemDic.update(adddes)
        print(itemDic)
        results.append(itemDic)
        sleep(randint(2,5))

    print(results)
    # input_data_Tomongo('furniture','pinkoi',results)

    # with open('./{}.json'.format(thename.replace('/','')), 'w', encoding='utf-8') as f:
    #     json.dump(results, f, ensure_ascii=False, indent=2)
    return results

if __name__ == "__main__":
    url = 'https://www.pinkoi.com/product/Q7pE2Zfm?category=5&ref_itemlist=8QNVk85K'
    print(plus_des(url))

    # main_scrap()