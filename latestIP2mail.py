#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import re,urllib2
import time
import smtplib  
from email.mime.text import MIMEText  

from mysqlDB import *
from conf import *

class GetIP:

    ipUrl = ['http://pv.sohu.com/cityjson?','http://whois.pconline.com.cn/ipJson.jsp']

    
    def __init__(self):
        pass

    def getip(self):
        ip = ''
        try:
            ip = self.visit(self.ipUrl[0])
        except:
            ip = self.visit(self.ipUrl[1])

        return ip

    def visit(self,url):
        html = urllib2.urlopen(url).read()
        return re.search('\d+\.\d+\.\d+\.\d+',html).group(0)

    def __del__(self):
        pass

class EmailMsg:

    _mail_host = ''
    _mail_postfix = ''
    
    def __init__(self, mail_host, mail_postfix):
    
        self._mail_host = mail_host
        self._mail_postfix = mail_postfix

    
    def sendEmail(self, mailto, subject, content):  

        mail_list = mailto
        mail_user = username_mail       #用户名
        mail_passwd = password_mail       #密码
        
        sendfrom = '<' + mail_user + '@' + self._mail_postfix + '>'

        #Message 编辑正文
        msg = MIMEText(content,_subtype='plain',_charset='gb2312')  
        msg['Subject'] = subject
        msg['From'] = sendfrom
        msg['To'] = ";".join(mail_list)  
#       print msg

        try:  
            server = smtplib.SMTP()  
            server.connect(self._mail_host)  
            server.login(mail_user, mail_passwd)

            server.sendmail(sendfrom, mail_list, msg.as_string())  
            server.close()  

            return True  

        except Exception as e:  
            print str(e)  
            return False  


    def __del__(self):
        pass

def getLatestIPfromMysql():
    dbm = DBMonitor()
    dbm.selectDB('localInfo')
    sql = """select ip from localInfo.centosip as t   
                        where  dt=(
                            select max(t1.dt) from localInfo.centosip as t1)"""
    dbm.query(sql)
    dbm.commit()
    return dbm.fetchOne()

def updateCentosIP(ob):
    dbm = DBMonitor()
    dbm.selectDB('localInfo')
    for o in ob:
        dbm.replacePureData('centosip',['dt','ip'],o)
    dbm.commit()

if __name__ == '__main__':  
    
    # 获取公网ip
    getmyip = GetIP()
    ip = getmyip.getip()

    lastIP = getLatestIPfromMysql()[0]
    if ip != lastIP:

        print 'centos ip has been changed to:', ip
        #收件箱列表 
        mailto = receiveList
        subject = 'Today--IP'
        curTime =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        content = curTime + ' : ['+ip+']'
    
        #发送邮件
        em = EmailMsg(mail_host, mail_postfix)
        em.sendEmail(mailto, subject, content)
        updateCentosIP([(curTime, ip)])
    else:
        print 'centos ip is not changed, it is still:', lastIP
