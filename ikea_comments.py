from random import randint
import requests
import json
from user_agent import generate_user_agent
from time import sleep

#讀入JSON找尋商品ID
with open('json_footstools_01.json', 'r', encoding='utf8') as f:
    ikeaJson = json.load(f)
#將ID存成LIST
itemsid = [data['id'] for data in ikeaJson]
end = []
#批次讀入ID
for theid in itemsid:
    itemid = int(theid)
    print(itemid)
    # itemid = '20266683'
    firsturl = 'https://display.powerreviews.com/m/43967/l/zh_TW/product/{}/reviews?apikey=1e9ad068-6739-4743-921c-7433b46b48ff&_noconfig=true'.format(itemid)
    headers = {'User-Agent': generate_user_agent()}
    firstres = requests.get(firsturl, headers=headers)
    firstJson = json.loads(firstres.text)
    results = {'id':itemid}

    page_number = firstJson['paging']['total_results'] #取出貼文數
    print(page_number)

    if page_number == 0:
        results['comments'] = 'Nocomments'
        end.append(results)
        print(results)

    else:
        for i in range(0,page_number, 25):
            # print(i)
            # itemid = int(theid)
            page = i
            url = 'https://display.powerreviews.com/m/43967/l/zh_TW/product/{}/reviews?paging.from={}&paging.size=25&_noconfig=true&apikey=1e9ad068-6739-4743-921c-7433b46b48ff'.format(itemid, page)
                
            headers = {'User-Agent': generate_user_agent()}
            res = requests.get(url, headers=headers)
            comm = json.loads(res.text)

            dic = {}
            for idx, contents in enumerate(comm['results'][0]['reviews']):
                headline = contents['details']['headline']
                sub = contents['details']['comments']
                dic[f'comment{idx+1}']= {"Titile":f'{headline}',"sub":f'{sub}'}
            # print(dic)
            if dic!={}:
                for i, j in dic.items():
                    if j['sub'] == '':
                        del j['sub']
                results['comments'] = dic
            else:
                results['comments'] = 'Nocomments'
            
            end.append(results)
            print(results)
            sleep(randint(2,5))
    sleep(randint(1,5))

with open('./AllIdcomment.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(end, jsonfile, ensure_ascii=False, indent=2)