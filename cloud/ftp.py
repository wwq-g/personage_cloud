import MySQLdb
from django.db import connection


def get_data(sql):#获取数据库的数据
    # conn = MySQLdb.connect('127.0.0.1','root','zxcv','personage_cloud',port=3306)   #test为数据库名
    cur = connection.cursor()
    cur.execute(sql)
    results = cur.fetchall() # 搜取所有结果
    cur.close()
    connection.close()
    return results


def readFile(filename):
    with open(filename, 'rb') as f:
        while True:
            c = f.read()
            if c:
                yield c
            else:
                break