import pymysql

def check_col(columns):
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

    cursor.execute("use Homeset")
    sql = "select {} from items".format(columns)
    cursor.execute(sql)
    data = cursor.fetchall()

    # cursor.execute("select max(id) from items")
    # theId =  cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    datas ={d[0] for d in data}
    return datas
    # return theId, datas

if __name__ == '__main__':
    columns = 'url'
    results = check_col(columns)
    # num, results = check_col(columns)
    # print(num)
    print(results)


