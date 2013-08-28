#!/usr/bin/env python
import subprocess

baseDir = "/var/www/homelessgaffer.com/"

GIT_WORK_TREE = baseDir

pip freeze old
diff old new
if same
    print "no changes, skipping update"
else:
    pip install -r 
    print "updated it all"

rm /tmp/req.old
print "removed /tmp/req.old"

sudo service nginx restart
print "restarted nginx"

sudo service uwsgi restart
print "restarted uwsgi"
