#coding:utf-8

import sys 
reload(sys)
sys.setdefaultencoding('utf8')

import poplib
from email import parser
import email

import string
from mysqlDB import *
from conf import *

def updateSshConf():
    dbm = DBMonitor()
    dbm.selectDB('localInfo')
    sql = """update localInfo.sshconf
                set Hostname = (
                    select ip from localInfo.centosip as t   
                        where  dt=(
                            select max(t1.dt) from localInfo.centosip as t1)) 
                                where hostAlias = 'centos'"""
    dbm.query(sql)
    dbm.commit()
    return dbm.fetchOne()

def updateCentosIP(ob):
    dbm = DBMonitor()
    dbm.selectDB('localInfo')
    for o in ob:
        dbm.replacePureData('centosip',['dt','ip'],o)
    dbm.commit()

#Get messages from server:
def readIPemail():
    pop_conn = poplib.POP3_SSL(pop3host)
    pop_conn.user(username_mail)
    pop_conn.pass_(password_mail)
    
    dt_ip = set()
    msg_len = len(pop_conn.list()[1])
    for i in range(msg_len):
        message = parser.Parser().parsestr('\n'.join(pop_conn.retr(i+1)[1]))
        subject = message.get('subject')   
        if subject != 'Today--IP':
            continue
        for part in message.walk():
            contentType = part.get_content_type()
            if contentType == 'text/plain':# or contentType == 'text/html':
                #保存正文
                data = part.get_payload(decode=True)
                dt_ip.add((data[:19],data.split('[')[-1].split(']')[0]))
    pop_conn.quit()
    return dt_ip

if __name__ == '__main__':
    dt_ip=readIPemail()
    updateCentosIP(dt_ip)
    updateSshConf()
