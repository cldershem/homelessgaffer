import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
CSRF_ENABLED = True
SECRET_KEY = ('\xf8\xd4\x99\xbf\x900\xcb\xc6\xdc;\xf4\xe4\xadH' +
              '\xe2\xc6\x16\xd8\xfb\xd2\xb0/j\x97')
MONGODB_SETTINGS = {'DB': "homelessgaffer"}

dateTimeNow = datetime.datetime.utcnow()
