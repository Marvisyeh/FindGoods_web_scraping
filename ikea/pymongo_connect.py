from pymongo import MongoClient, collection, results
import pymongo
import json

connection = MongoClient(host='localhost', port=27017)

def con_mongo(db, columns, data):
    # # 連線mongodb
    thedb = connection.db
    collection = thedb['{}'.format(columns)]
    try: #存入資料庫
        result = collection.insert_one(data)        
        print("已新增",data)
    except Exception as err:
        print(err)


def input_data_Tomongo(db,column, datas):
    dblist = connection.list_database_names()
    if db not in dblist:
        print(f"{db}已建立")
    mydb = connection[db]
    collections = mydb.list_collection_names()
    if column not in collections:
        print(f"{column} already create")
    ## 單筆資料
    collection = mydb[column]
    try:
        result = collection.insert_one(datas)
        print(result.inserted_id)
    except pymongo.errors.DuplicateKeyError as e:
        print(e)
        print("已存在ID",datas['_id'])
    
    ## 存入多筆資料
    # collection = mydb[column]
    # for data in datas:
    #     try:
    #         result = collection.insert_one(data)
    #         print(result.inserted_id)
    #     except pymongo.errors.DuplicateKeyError as e:
    #         print(e)
    #         print("已存在ID",data['_id'])


#將JSON檔寫入MONGODB
def jsontoMongo(json_path, db,name):
    # 連線mongodb
    connection = MongoClient(host='localhost', port=27017)
    db = connection[db]
    # collection = db['footstools']

    with open(path, 'r', encoding='utf8') as f:
        datas = json.load(f)
    # print(len(datas))
    # print(datas)
    collections = db.list_collection_names()
    if name in collections:
        db.name.drop()
        # print("存在，已刪除")
        collection = db[name]
        result = collection.insert_many(datas)
        print(result.inserted_ids)

    else:
        # print("不存在")
        collection = db[name]
        result = collection.insert_many(datas)
        print(result.inserted_ids)
    # try: #存入資料庫
    #     collection.drop()
    #     result = collection.insert_many(datas)        
    #     print("已新增")

    # except Exception as e:
    #     print(e)
    #     # print('已存在')


def mongo_data(db,column):
    connection = MongoClient(host='localhost', port=27017)
    dbs = connection[db]
    thedb = dbs[column]
    result = thedb.find()
    return result


#檢查URL是否重複
def url_set_1(db, columns):
    dbs = mongo_data(db, columns)
    url = {db['url'] for db in dbs}
    return url

#檢查id是否重複
def url_set(db, columns):
    dbs = mongo_data(db, columns)
    url = {db['url'] for db in dbs}

    if bool(url) == True:
        dbs = mongo_data(db, columns)
        # print(bool(url))
        idx =max([db['_id'] for db in dbs])+1
    else:
        idx = 1
    return idx,url

if __name__ == '__main__':
    db = "hs"
    columns = "trp"
    idx,url = url_set(db, columns)
    print(idx,url)
    # dbs = url_set(db,columns)
    # db = max([db['_id'] for db in dbs])
    # print(db)
    # print([i for i in mongo_data(db,column)])
    # print(mongo_data(db, column))
    # datas = [{"_id":1}]

    # con_mongo(db, columns, data)

    # input_data_Tomongo(db,column,datas)


    # result = mongo_data(db, column)
    # print(result)
    # print(result[0]['url'].split('.')[1])
    # for results in result:
    #     print(results['name'],len(results['name']))
    #     print(results['id'])
    #     print(results['price'])
    #     print(results['brand'],len(results['brand']))
    #     print(results['extraFacts'].split(',')[1],len(results['extraFacts'].split(',')[1]))
    #     print(results['url'])
    #     name = results['name']
    #     itemid = results['id']
    #     price = results['price']
    #     brand = results['brand']
    #     extraFacts = results['extraFacts'].split(',')[1]
    #     url = results['url']






