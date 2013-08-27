import os
import datetime
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
CSRF_ENABLED = True
SECRET_KEY = secrets.SECRET_KEY
MONGODB_SETTINGS = {'DB': "homelessgaffer"}

dateTimeNow = datetime.datetime.utcnow()

#RECAPTCHA_USE_SSL
RECAPTCHA_PUBLIC_KEY = secrets.RECAPTCHA_PUBLIC_KEY
RECAPTCHA_PRIVATE_KEY = secrets.RECAPTCHA_PRIVATE_KEY
RECAPTCHA_OPTIONS = {'theme': 'white'}
