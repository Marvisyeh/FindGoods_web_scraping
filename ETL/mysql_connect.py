from pymongo import results
import pymysql
from pymongo_connect import mongo_data
from  check import check_col

connInfo = {
    'host': 'localhost',
    'port': 3306,
    'user': 'TFI101',
    'passwd': 'tfi101',
    'db':'IKEA',
    'charset': 'utf8mb4'
}

conn = pymysql.connect(**connInfo)
cursor = conn.cursor()
cursor.execute("create database if not exists Homeset")
cursor.execute("use Homeset")
cursor.execute("""CREATE TABLE IF NOT EXISTS items (
    ID           INT NOT NULL AUTO_INCREMENT,
    NAME         VARCHAR(50),
    ITEMID       INT NOT NULL,
    PRICE        INT,
    BRAND        VARCHAR(15),
    COLORTYPE    VARCHAR(25),
    URL          TEXT,
    CONSTRAINT items_PRIMARY_KEY PRIMARY KEY (ID)
)ENGINE=INNODB AUTO_INCREMENT=1001 """)

result = mongo_data('HomeSet','footstools')
theId, urled = check_col('url')

for results in result:
    name = results['name']
    itemid = results['id']
    price = results['price']
    brand = results['brand']
    extraFacts = results['extraFacts'].split(',')[1]
    url = results['url']
    datas = (name, itemid, price, brand, extraFacts, url)
    
    insert_commit = """INSERT INTO items (NAME, ITEMID, PRICE, BRAND, COLORTYPE, URL)
    VALUES (%s, %s, %s, %s, %s, %s)"""
    if url in urled:
        print("url already exists")
        continue
    else:
        
        cursor.execute(insert_commit, datas)
        conn.commit()
        print(f"Insert into {datas}")

cursor.close()
conn.close()
