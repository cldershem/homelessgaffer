from flask import (Blueprint, render_template, flash, request,
                   redirect, url_for)
from jinja2 import TemplateNotFound
from app.models import Unity, Comment, User
# from app.forms import UnityForm
from app.constants import DATE_TIME_NOW
from app.utils import makeSlug, markRight
from flask.ext.login import login_required, current_user
from flask.ext.mongoengine import Pagination
from app import app

mod = Blueprint('unity', __name__, url_prefix='/unity')


@mod.route('/', defaults={'tag': None, 'user': None, 'pageNum': 1})
@mod.route('/listposts', defaults={'tag': None, 'user': None, 'pageNum': 1})
@mod.route('/listposts/pageNum/<int:pageNum>',
           defaults={'tag': None, 'user': None})
@mod.route('/listposts/tag/<tag>', defaults={'user': None, 'pageNum': 1})
@mod.route('/listposts/tag/<tag>/pageNum/<int:pageNum>',
           defaults={'user': None})
@mod.route('/listposts/user/<user>', defaults={'tag': None, 'pageNum': 1})
@mod.route('/listposts/user/<user>/pageNum/<int:pageNum>',
           defaults={'tag': None})
def listPosts(tag, user, pageNum):
    # if postToBlog:
    #     display list with preview
    # if !postToBlog:
    #     display list of titles in order of recently edited
    # if tag or if user:
    #     display list of both
    unityPages = Unity.objects.all()
    return render_template('unity/listUnity.html',
                           page="listUnity",
                           pages=unityPages)
