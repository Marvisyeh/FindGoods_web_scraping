from random import randint
import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import json
from time import sleep
from pinkoi_insideItem import plus_des

final = []
url = 'https://www.pinkoi.com/browse?category=5&subcategory=543'
for i in range(1,2):
    headers = {'User-Agent' : generate_user_agent()}
    res = requests.get(url, headers = headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    inside_list = []
    for i in soup.select('script[type="application/ld+json"]'):
        for j in i.contents:
    #         print(j['name'])
            inside_list.append(json.loads(j))
    itemList=inside_list[1:]
    final.extend(itemList)
        
    path=inside_list[0]
    url = soup.select('link[rel="next"]')[0]['href']
    sleep(randint(1,4))
# print(final)
name_1 = [n['name'] for n in [p['item'] for p in path['itemListElement']]]
thename = '_'.join(name_1)

results = []
for idx,i in enumerate(final):
#     print(idx,i)
    url = i['offers']['url']
    adddes = plus_des(url)
    itemDic={}
    itemDic['_id']=idx+1
    itemDic.update(i)
    itemDic.update(adddes)
#     print(itemDic)
    results.append(itemDic)
    sleep(randint(2,5))

with open('./{}'.format(thename.replace('/','')), 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(len(results))