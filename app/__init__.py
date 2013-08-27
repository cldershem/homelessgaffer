from flask import Flask
#from config import basedir
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.principal import Principal

app = Flask(__name__)
app.config.from_object('config')

db = MongoEngine(app)
lm = LoginManager(app)
lm.login_view = "login"
bcrypt = Bcrypt(app)
principals = Principal(app)

#if not app.debug:
from app import routes, models, admin  # nopep8
