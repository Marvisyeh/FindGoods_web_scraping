import os 
from random import choice
from pymongo import MongoClient, collection, results
import pymongo

connection = MongoClient(host='localhost', port=27017)

# readfile
with open('./fakedatas.csv', 'r', encoding='utf8') as f:
    # print(f.read())
    data = f.read()

datas = data.split('\n')[1:]
datas = [i.split(',') for i in datas]
userId = {i[0] for i in datas if i[0] != ''}
result = []
for i in userId:
    result.append({'_id':i, 'click':{}})


a = 2,4,6
for re in result:
    for data in datas:
        if data[0] == re['_id']:
            re['click'].update({data[1]:float(data[2])*choice(a)})



# # 連線mongodb
thedb = connection.user
collection = thedb['userinfo']
try: #存入資料庫
    for i in result:
        result = collection.insert_one(i)        
        print("已新增",data)
except Exception as err:
    print(err)