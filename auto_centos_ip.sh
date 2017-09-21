#/bin/bash

/usr/bin/python /Users/DoraZhang/Documents/github/host-ssh-admin/fromMail2DB_SSH_conf.py
/usr/bin/python /Users/DoraZhang/Documents/github/host-ssh-admin/db_SSH_conf2file.py

#10 9 * * * /usr/bin/python /Users/DoraZhang/Documents/github/host-ssh-admin/fromMail2DB_SSH_conf.py
#15 9 * * * /usr/bin/python /Users/DoraZhang/Documents/github/host-ssh-admin/db_SSH_conf2file.py
