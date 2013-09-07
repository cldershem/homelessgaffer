from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.mail import Mail

app = Flask(__name__)
app.config.from_object('config')

db = MongoEngine(app)
lm = LoginManager(app)
lm.login_view = "login"
bcrypt = Bcrypt(app)
toolbar = DebugToolbarExtension(app)
mail = Mail(app)

#if not app.debug:
from app import routes, models, admin  # nopep8
