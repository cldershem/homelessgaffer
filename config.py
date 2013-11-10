import os
import secrets


DEBUG = True
TESTING = False

# misc
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

ADMINS = secrets.ADMINS

# wtforms
CSRF_ENABLED = True
SECRET_KEY = secrets.SECRET_KEY

# db
MONGODB_SETTINGS = {'DB': "homelessgaffer"}

# recaptcha
#RECAPTCHA_USE_SSL
RECAPTCHA_PUBLIC_KEY = secrets.RECAPTCHA_PUBLIC_KEY
RECAPTCHA_PRIVATE_KEY = secrets.RECAPTCHA_PRIVATE_KEY
RECAPTCHA_OPTIONS = {'theme': 'white'}

# flask debug toolbar
DEBUG_TB_PANELS = [
    'flask_debugtoolbar.panels.versions.VersionDebugPanel',
    'flask_debugtoolbar.panels.timer.TimerDebugPanel',
    'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
    'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
    'flask_debugtoolbar.panels.template.TemplateDebugPanel',
    #'flask_debugtoolbar.panels.sqlalchemy.SQLAlchemyDebugPanel',
    'flask_debugtoolbar.panels.logger.LoggingPanel',
    'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
    'flask_debugtoolbar_mongo.panel.MongoDebugPanel',
    ]
DEBUG_TB_INTERCEPT_REDIRECTS = False

# mail server settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = secrets.MAIL_USERNAME
MAIL_PASSWORD = secrets.MAIL_PASSWORD

# oauth keys
FACEBOOK_CONSUMER_KEY = secrets.SOCIAL_FACEBOOK['consumer_key']
FACEBOOK_CONSUMER_SECRET = secrets.SOCIAL_FACEBOOK['consumer_secret']
GOOGLE_CONSUMER_KEY = secrets.SOCIAL_GOOGLE['consumer_key']
GOOGLE_CONSUMER_SECRET = secrets.SOCIAL_GOOGLE['consumer_secret']
