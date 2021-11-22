from pymongo import MongoClient, results
import pymongo
import json
def mongo_data(db,collection):
    connection = MongoClient(host='localhost', port=27017)
    dbs = connection[db]
    db = dbs[collection]

    result = db.find()
    return result


if __name__ == '__main__':
    result = mongo_data('HomeSet','footstools')
    for results in result:
        # print(results['name'],len(results['name']))
        # print(results['id'])
        # print(results['price'])
        print(results['brand'],len(results['brand']))
        # print(results['extraFacts'].split(',')[1],len(results['extraFacts'].split(',')[1]))
        # print(results['url'])
    #     name = results['name']
    #     itemid = results['id']
    #     price = results['price']
    #     brand = results['brand']
    #     extraFacts = results['extraFacts'].split(',')[1]
    #     url = results['url']






