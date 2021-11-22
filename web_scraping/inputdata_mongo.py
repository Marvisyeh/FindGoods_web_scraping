from pymongo import MongoClient
import pymongo

connection = MongoClient(host='localhost', port=27017)

def input_data_Tomongo(db,column, datas):
    dblist = connection.list_database_names()
    if db in dblist:
        print(f"{db}已存在")
    mydb = connection[db]
    collections = mydb.list_collection_names()
    if column in collections:
        print(f"{column} already exists")
    collection = mydb[column]
    for data in datas:
        try:
            result = collection.insert_one(data)
            print(result.inserted_id)
        except pymongo.errors.DuplicateKeyError as e:
            print(e)
            print("已存在ID",data['_id'])

if __name__ == "__main__":
    db = "HomeSet"
    column = "footstools"
    datas = [{"_id":1}]
    input_data_Tomongo(db,column,datas)