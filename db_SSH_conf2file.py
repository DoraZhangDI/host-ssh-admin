#coding:utf-8

import sys 
reload(sys)
sys.setdefaultencoding('utf8')

from mysqlDB import *
from conf import *

def getAllSHH_conf():
    dbm = DBMonitor()
    dbm.selectDB('localInfo')
    sql = "select hostAlias,Hostname,username,PreferredAuthentications,IdentityFile,portno from sshconf;"
    dbm.query(sql)
    results = dbm.fetchAll()
    sshconf = []
    for r in results:
        sshconf.append({r[0]:{'Hostname':r[1],'User':r[2],'PreferredAuthentications':r[3],'IdentityFile':r[4],'Port':r[5]}})
    return sshconf

def write2sysout(sc):
    for kv in sc:
        for k,v in kv.items():
            print 'Host',k
            for kk,vv in v.items():
                if vv != '':
                    print '\t'+kk,vv
            print ''

def write2ssh_conf(sc):
    sshconf_path = '/Users/DoraZhang/.ssh/config'
    f = open(sshconf_path,'w')
    for kv in sc:
        for k,v in kv.items():
            print >> f, 'Host',k
            for kk,vv in v.items():
                if vv != '':
                    print >> f, '\t',kk,vv
            print >> f, ''

if __name__ == '__main__':
    sc = getAllSHH_conf()
    write2ssh_conf(sc)
#    write2sysout(sc)
