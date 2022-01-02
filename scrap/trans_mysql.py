import pymysql,pymongo,re
from pymongo import MongoClient, collection, results

connection = MongoClient(host='localhost', port=27017)
connInfo = {
        'host': 'localhost',
        'port': 3306,
        'user': '',
        'passwd': '',
        'charset': 'utf8mb4'
    }

def mongo_data(db,column):
    dbs = connection[db]
    thedb = dbs[column]
    result = thedb.find()
    return result

def site_judge(url):
    w = url.split('.')[1]
    if w == 'ikea':
        return '10'
    elif w == 'trplus':
        return '20'
    elif w == 'pinkoi':
        return '30'
    else:
        return w

def check_url(db='homeset', columns='items'):

    conn = pymysql.connect(**connInfo)
    cursor = conn.cursor()
    try:
        # cursor.execute("use {}".format(db))
        sql = "select url from {}.{}".format(db,columns)
        cursor.execute(sql)
        data = cursor.fetchall()

        # cursor.execute("select max(id) from items")
        # theId =  cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        datas ={d[0] for d in data}
        return datas
    except pymysql.err.ProgrammingError as e:
        print(e)
        datas = {}
        return datas

def tomysql(db, columns, schema):
    conn = pymysql.connect(**connInfo)
    cursor = conn.cursor()
    cursor.execute("create database if not exists {}".format(schema))
    cursor.execute("use {}".format(schema))
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS item (
        `ITEMNO` INT NOT NULL AUTO_INCREMENT,
        `ITEMNAME` VARCHAR(100) NOT NULL,
        `ITEMID` INT NOT NULL,
        `PRICE` DECIMAL(7,2),
        `BRAND` VARCHAR(50) NULL,
        `URL` VARCHAR(2083) NOT NULL,
        `IMG_PATH` VARCHAR(128) NOT NULL,
        `PFNO` INT NOT NULL,
        `TAGS` VARCHAR(100) NULL,
        `CATE` VARCHAR(20) NULL,
        PRIMARY KEY (`ITEMNO`))
        AUTO_INCREMENT=1001 DEFAULT CHARACTER SET = utf8mb4;""")

    results = mongo_data(db,columns)
    urled = check_url(schema,'item')

    for result in results:
        ITEMNAME = result['name']
        ITEMID = result['id']
        PRICE = result['price']
        BRAND = result['brand']
        CATE = ' '.join(re.sub('\W+',' ',result['cn_title']).split())
        URL = result['url']
        # IMG_PATH = result['imgs'][0]
        try:
            IMG_PATH = result['imgurl'][0]
        except:
            print(URL,result['imgs'])
        PFNO = site_judge(URL)
        # tags = re.sub('\W+',',',re.sub('[a-zA-z]+|\d+..','',result['cn_title']))
        # tags = ''
        # print(tags[:])
        datas = (ITEMNAME, ITEMID, PRICE, BRAND, URL, IMG_PATH,columns, CATE, PFNO)
        # print(datas)
        insert_commit = """INSERT INTO item (ITEMNAME, ITEMID, PRICE, BRAND, URL, IMG_PATH, CATE, TAGS, PFNO)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        if URL in urled:
            print("url already exists")
            continue
        else:
            cursor.execute(insert_commit, datas)
            conn.commit()
            print(f"Insert into {datas}")

if __name__ == '__main__':
    # db = 'trplus'
    db = 'ikea2'
    columns = ['vasesbowl', 'frame', 'lamps', 'footstool', 'Cushion', 'mugs', 'desk']
    x=1
    for i in columns:
        tomysql(db, i, 'SHOPDB')
        print(x)
        x+=1