from random import randint
import requests
import json
from user_agent import generate_user_agent
from time import sleep

with open('jason_ikea.json', 'r', encoding='utf8') as f:
    ikeaJson = json.load(f)

itemsid = [data['id'] for data in ikeaJson]
# print(itemsid)

end = {}
returnResult = []

for num, theid in enumerate(itemsid):
    firsturl = 'https://display.powerreviews.com/m/43967/l/zh_TW/product/{}/reviews?apikey=1e9ad068-6739-4743-921c-7433b46b48ff&_noconfig=true'.format(theid)
    # print(firsturl)
    headers = {'User-Agent': generate_user_agent()}
    firstres = requests.get(firsturl, headers=headers)
    firstJson = json.loads(firstres.text)
    page_number = firstJson['paging']['total_results']
    print(page_number)
    
    wraper = {}
    wraper['id']=num
    
    for i in range(0,page_number, 25):
        print(i)
        itemid = int(theid)
        page = i
        url = 'https://display.powerreviews.com/m/43967/l/zh_TW/product/{}/reviews?paging.from={}&paging.size=25&_noconfig=true&apikey=1e9ad068-6739-4743-921c-7433b46b48ff'.format(itemid, page)
        
        res = requests.get(url, headers=headers)
        comm = json.loads(res.text)
        
        dic = {}
        for idx, contents in enumerate(comm['results'][0]['reviews']):
            headline = contents['details']['headline']
            sub = contents['details']['comments']
            dic[f'comment{idx+1}']= {"headline":f'{headline}',"sub":f'{sub}'}
        # print(num, dic)
        if dic!={}:
            for i, j in dic.items():
                if j['sub'] == '':
                    del j['sub']
            end['comments'] = dic
        else:
            end['comments'] = 'Nocomments'
        sleep(randint(2,5))

sleep(randint(2,5))

wraper.update(end)
with open('comment.json', 'w') as f:
    f.write(json.dumps(wraper))
# print(wraper)