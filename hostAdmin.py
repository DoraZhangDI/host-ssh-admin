#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from mysqlDB import *

def savedb():
    dbm = DBMonitor()
    dbm.selectDB('localInfo')
    dbm.query('select * from hosts')
    results = dbm.fetchAll()
    for rr in results:
        print rr[0],rr[1]
savedb()
