from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.mail import Mail
from flask_oauth import OAuth
from flask.ext.pagedown import PageDown
from socket import gethostname

app = Flask(__name__)
app.config.from_object('config')

if gethostname() == 'cldershem-laptop':
    app.config['DEBUG'] = True
else:
    app.config['DEBUG'] = False

db = MongoEngine(app)
bcrypt = Bcrypt(app)
toolbar = DebugToolbarExtension(app)
mail = Mail(app)
lm = LoginManager(app)
lm.login_view = "users.login"
oauth = OAuth()
pagedown = PageDown(app)


# if not app.debug:
#     import config
#     import logging
#     from logging.handlers import SMTPHandler
#     from logging.handlers import RotatingFileHandler

#     # log mailer
#     credentials = None
#     if config.MAIL_USERNAME or config.MAIL_PASSWORD:
#         credentials = (config.MAIL_USERNAME, config.MAIL_PASSWORD)
#     mail_handler = SMTPHandler(
#         (config.MAIL_SERVER, config.MAIL_PORT),
#         'no-reply@' + config.MAIL_SERVER,
#         config.ADMINS, 'hg failure',
#         credentials)
#     mail_handler.setLevel(logging.ERROR)
#     app.logger.addHandler(mail_handler)

#     # log writer
#     file_handler = RotatingFileHandler(
#         'tmp/logs/hg.log',
#         'a',
#         1 * 1024 * 1024,
#         10)
#     file_handler.setLevel(logging.INFO)
#     file_handler.setFormatter(logging.Formatter(
#         '%(asctime)s %(levelname)s: %(message)s \
#         [in %(pathname)s:(lineno)d]'))
#     app.logger.setLevel(logging.INFO)
#     app.logger.addHandler(file_handler)
#     app.logger.info('hg startup')


from app import routes, models, admin  # nopep8
from app.admin import views  # nopep8
