import os
import secrets


DEBUG = True

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

# flask-security config
SECURITY_PASSWORD_HASH = "bcrypt"
SECURITY_EMAIL_SENDER = ADMINS[0]
SECURITY_LOGIN_URL = "users.login"
SECURITY_LOGOUT_URL = "users.logout"
SECURITY_REGISTER_URL = "users.register"
SECURITY_RESET_URL = "users.reset_password"
SECURITY_CONFIRM_URL = "users.activate_user"
SECURITY_POST_LOGIN_VIEW = "users.profile"
SECURITY_POST_LOGOUT_VIEW = "/"
SECURITY_FORGOT_PASSWORD_TEMPLATE = "users/forgotPassword.html"
SECURITY_LOGIN_USER_TEMPLATE = "users/login.html"
SECURTIY_REGISTER_USER_TEMPLATE = "users/register.html"
SECURITY_RESET_PASSWORD_TEMPLATE = "users/resetPassword.html"
#SECURITY_SEND_CONFIRMATION_TEMPLATE = "users/"
SECURITY_SEND_LOGIN_TEMPLATE = "users/"
SECURITY_SEND_REGISTER_EMAIL = True
SECURITY_CONFIRM_EMAIL_WITHIN = "5 days"
SECURITY_RESET_PASSWORD_WITHIN = "1 days"
hgPrefix = "[homelessgaffer] - "
SECURITY_EMAIL_SUBJECT_REGISTER = hgPrefix + "Welcome."
SECURITY_EMAIL_SUBJECT_PASSWOD_NOTICE = (
    hgPrefix + "Your password has been reset.")
SECURITY_EMAIL_SUBJECT_PASSWORD_RESET = (
    hgPrefix + "Reset Password Instructions.")
SECURITY_EMAIL_SUBJECT_PASSWORD_CHANGE_NOTICE = (
    hgPrefix + "Your password has been changed.")
SECURITY_EMAIL_SUBJECT_CONFIRM = (
    hgPrefix + "Please confirm your email address.")

# flask-social api keys
SOCIAL_FACEBOOK = secrets.SOCIAL_FACEBOOK
SOCIAL_GOOGLE = secrets.SOCIAL_GOOGLE
