import pymysql

connInfo = {
        'host': 'localhost',
        'port': 3306,
        'user': 'TFI101',
        'passwd': 'tfi101',
        'db':'furniture',
        'charset': 'utf8mb4'
    }

def select(shop):
    conn = pymysql.connect(**connInfo)
    cursor = conn.cursor()



    if shop == 'All Shop':
        cursor.execute("select i.name, i.price, i.url, i.img from items i join shop s on i.SITE = s.shopid")
        conn.commit()
        datas = cursor.fetchall()
        cursor.close()
        conn.close()
        return datas
    else:
        sql = """select i.name, i.price, i.url, i.img from items i
            join shop s on i.SITE = s.shopid
            where s.shopname = %s;"""
        cursor.execute(sql,shop)
        conn.commit()
        datas = cursor.fetchall()
        cursor.close()
        conn.close()
        return datas


if __name__ == "__main__":
    data = select('ikea')
    print(data)