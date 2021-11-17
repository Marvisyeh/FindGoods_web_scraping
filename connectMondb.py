from pymongo import MongoClient
import pymongo
import json
# 連線mongodb
connection = MongoClient(host='localhost', port=27017)
db = connection['HomeSet']
# collection = db['footstools']

with open('./json_footstools.json', 'r', encoding='utf8') as f:
    datas = json.load(f)
# print(len(datas))
# print(datas)
collections = db.list_collection_names()
if "footstools" in collections:
    db.footstools.drop()
    # print("存在，已刪除")
    collection = db['footstools']
    result = collection.insert_many(datas)
    print(result.inserted_ids)

else:
    # print("不存在")
    collection = db['footstools']
    result = collection.insert_many(datas)
    print(result.inserted_ids)
# try: #存入資料庫
#     collection.drop()
#     result = collection.insert_many(datas)        
#     print("已新增")

# except Exception as e:
#     print(e)
#     # print('已存在')
