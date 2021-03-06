"""
    app
    ~~~~~~~~~

    A mini-cms built using Flask.

    :copyright: and :license: see TOPMATTER.
"""

from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.mail import Mail
from flask_oauth import OAuth
from flask.ext.pagedown import PageDown

app = Flask(__name__)
app.config.from_object('config')

db = MongoEngine(app)
bcrypt = Bcrypt(app)
toolbar = DebugToolbarExtension(app)
mail = Mail(app)
lm = LoginManager(app)
lm.login_view = "users.login"
oauth = OAuth()
pagedown = PageDown(app)

from app import routes, models, admin  # nopep8
from app.admin import views  # nopep8
