import pymysql

def check_url(db, columns):
    connInfo = {
        'host': 'localhost',
        'port': 3306,
        'user': 'TFI101',
        'passwd': 'tfi101',
        'charset': 'utf8mb4'
    }

    conn = pymysql.connect(**connInfo)
    cursor = conn.cursor()
    try:
        cursor.execute("use {}".format(db))
        sql = "select url from {}".format(columns)
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
    # return theId, datas

if __name__ == '__main__':
    db = 'HomeSet'
    columns = 'footstool_main'
    results = check_url(db, columns)
    # num, results = check_col(columns)
    # print(num)
    print(results)


