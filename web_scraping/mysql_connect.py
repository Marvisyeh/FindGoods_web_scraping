import pymysql
from pymongo_connect import mongo_data
from check import check_url
from tool import site_judge

connInfo = {
        'host': 'localhost',
        'port': 3306,
        'user': 'TFI101',
        'passwd': 'tfi101',
        'charset': 'utf8mb4'
    }


def create(sql, type=False):
    conn = pymysql.connect(**connInfo)
    cursor = conn.cursor()
    if type == True:
        cursor.executemany(sql)
    else:
        cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()



def input_mySQL(db, columns, pinkoi=False):
    conn = pymysql.connect(**connInfo)
    cursor = conn.cursor()
    cursor.execute("create database if not exists {}".format(db))
    cursor.execute("use {}".format(db))
    cursor.execute("""CREATE TABLE IF NOT EXISTS items (
        ID          INT NOT NULL AUTO_INCREMENT,
        NAME        VARCHAR(255),
        ITEMID      VARCHAR(30) NOT NULL,
        PRICE       INT,
        BRAND       VARCHAR(50),
        URL         TEXT,
        IMG         TEXT,
        SITE        VARCHAR(8),
        CONSTRAINT items_PRIMARY_KEY PRIMARY KEY (ID) 
    )ENGINE=INNODB AUTO_INCREMENT=1001 """)

    result = mongo_data(db,columns)
    urled = check_url(db,columns)


    if pinkoi == True:
        for results in result:
            name = results['name']
            itemid = results['productID']
            price = results['offers']['price']
            brand = results['offers']['seller']['name']
            # extraFacts = results['extraFacts'].split(',')[1]
            url = results['offers']['url']
            img = results['imgurl'][0]
            site = site_judge(url)
            datas = (name, itemid, price, brand, url, img, site)
            
            insert_commit = """INSERT INTO items (NAME, ITEMID, PRICE, BRAND, URL, IMG, SITE)
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            if url in urled:
                print("url already exists")
                continue
            else:
                cursor.execute(insert_commit, datas)
                conn.commit()
                print(f"Insert into {datas}")

    else:
        for results in result:
            # name = results['name']
            name = results['itemtitle']#trplus
            # name = "-".join(results['name'].split(' ')[0:2])
            # itemid = results['id']
            itemid = results['itemId']#trplus
            price = results['price']
            brand = results['brand']
            # extraFacts = results['extraFacts'].split(',')[1]
            url = results['url']
            img = results['imgurl'][0]
            site = site_judge(url)
            datas = (name, itemid, price, brand, url, img, site)
            
            insert_commit = """INSERT INTO items (NAME, ITEMID, PRICE, BRAND, URL, IMG, SITE)
            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            if url in urled:
                print("url already exists")
                continue
            else:
                cursor.execute(insert_commit, datas)
                conn.commit()
                print(f"Insert into {datas}")

    cursor.close()
    conn.close()

if __name__ == '__main__':
    db = 'furniture'
    # columns = 'ikea'
    # columns = 'trplus'
    columns = 'pinkoi'
    input_mySQL(db, columns, True)

    # db = 'HomeSet'
    # columns = 'trplus'
    # input_mySQL(db, columns)

    # db = 'HomeSet'
    # columns = 'pinkoi'
    # input_mySQL(db, columns, ver=True)