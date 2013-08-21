from flask import Flask
from config import basedir
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

db = MongoEngine(app)
lm = LoginManager(app)
lm.login_view = "login"

from app import routes, models
