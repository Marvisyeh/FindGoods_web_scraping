from pymongo_connect import mongo_data
import re

#IKEA

results = mongo_data('furniture','ikea')


for result in results:
    name = ("-".join(result['name'].split(' ')[0:2]))
    id =(result['id'])
    price = (result['price'])
    brand = (result['brand'])
    url = (result['url'])
    imgurl = (result['imgurl'][0])
    
    data = [name, id, price, brand, url, imgurl]
    print(data)


#pinkoi
# results = mongo_data('furniture','pinkoi')

# for result in results:
#     # print(result)
#     name = (result['name'])
#     print(result['productID'])
#     print(result['offers']['price'])
#     print(result['offers']['seller']['name'])
#     print(result['offers']['url'])
#     print(result['imgurl'][0])
# # print(results[0])


    # name = ("-".join(result['name'].split(' ')[0:2]))
    # id =(result['id'])
    # price = (result['price'])
    # brand = (result['brand'])
    # url = (result['url'])
    # imgurl = (result['imgurl'][0])
    
    # data = [name, id, price, brand, url, imgurl]
    # print(data)