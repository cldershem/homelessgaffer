from flask import (Blueprint, render_template, flash, request,
                   redirect, url_for)
from jinja2 import TemplateNotFound
from app.models import Unity, User, Comment
from app.forms import UnityForm, CommentForm
from app.constants import DATE_TIME_NOW
from app.utils import makeSlug
from flask.ext.login import login_required, current_user
from flask.ext.mongoengine import Pagination

mod = Blueprint('unity', __name__, url_prefix='/unity')


@mod.route('/', defaults={'tag': None, 'user': None, 'pageNum': 1})
@mod.route('/blog', defaults={'tag': None, 'user': None, 'pageNum': 1})
@mod.route('/listposts', defaults={'tag': None, 'user': None, 'pageNum': 1})
@mod.route('/listposts/page/<int:pageNum>',
           defaults={'tag': None, 'user': None})
@mod.route('/listposts/tag/<tag>', defaults={'user': None, 'pageNum': 1})
@mod.route('/listposts/tag/<tag>/page/<int:pageNum>', defaults={'user': None})
@mod.route('/listposts/user/<user>', defaults={'tag': None, 'pageNum': 1})
@mod.route('/listposts/user/<user>/page/<int:pageNum>', defaults={'tag': None})
def listUnity(tag, user, pageNum):
    if tag:
        unitySet = Pagination(
            Unity.get_set(postType='blog', tags=tag),
            pageNum, 10)
        pageTitle = tag
    if user:
        user = User.get(email=user)
        unitySet = Pagination(
            Unity.get_set(postType='blog', author=user),
            pageNum, 10)
        pageTitle = user.email
    elif not tag and not user:
        unitySet = Pagination(
            Unity.get_set(postType='blog'),
            pageNum, 10)
        pageTitle = "blog"  # "listUnity"
    return render_template('unity/listUnity.html',
                           pageTitle=pageTitle,
                           unitySet=unitySet,
                           page=pageNum)


@mod.route('/newunity', methods=['GET', 'POST'])
@login_required
def newUnity():
    form = UnityForm()

    if request.method == 'POST':
        if not form.validate_with_slug():
            return render_template("unity/newUnity.html",
                                   form=form,
                                   pageTitle="newUnity")
        else:
            slug = makeSlug(form.title.data)
            newUnity = Unity(title=form.title.data,
                             slug=slug,
                             body=form.body.data,
                             postType=form.postType.data)
            if form.tags.data:
                newUnity.tags = form.tags.data
            if form.source.data:
                newUnity.source = form.source.data
            if form.summary.data:
                newUnity.summary = form.summary.data
            newUnity.author = User.get(email=current_user.email)
            newUnity.save()
            flash('Your unity has been posted.')
            return redirect(url_for('.staticUnity', slug=slug))
    elif request.method == 'GET':
        return render_template("unity/newUnity.html",
                               form=form,
                               pageTitle="newUnity")


@mod.route('/<slug>/edit', methods=['GET', 'POST'])
@login_required
def editUnity(slug):
    unity = Unity.get(slug=slug)
    slug = unity.slug
    form = UnityForm(obj=unity)

    if request.method == 'POST':
        if not form.validate_on_update(slug):
            return render_template('unity/newUnity.html',
                                   pageTitle=unity.title,
                                   slug=slug,
                                   form=form)
        else:
            form.populate_obj(unity)
            unity.edited_on.append(DATE_TIME_NOW)
            unity.save()
            flash("Your page has been updated.")
            return redirect(url_for('.staticUnity', slug=slug))
    elif request.method == 'GET':
        form.populate_obj(unity)
        return render_template('unity/newUnity.html',
                               pageTitle=unity.title,
                               slug=slug,
                               form=form)


@mod.route('/<slug>', methods=['GET', 'POST'])
def staticUnity(slug):
    if request.method == 'POST':
        unity = Unity.get_or_404(slug=slug)
        form = CommentForm()
        if not form.validate():
            return render_template('unity/staticUnity.html',
                                   pageTitle=unity.title,
                                   unity=unity,
                                   form=form)
        else:
            newComment = Comment(body=form.comment.data)
            newComment.author = User.get(email=current_user.email)
            unity.comments.append(newComment)
            unity.save()
            form.comment.data = None  # resets field on refresh
            flash('Comment Posted')
        return render_template('unity/staticUnity.html',
                               pageTitle=unity.title,
                               unity=unity,
                               form=form)
    elif request.method == 'GET':
        try:
            return render_template('unity/%s.html' % slug,
                                   pageTitle=slug)
        except TemplateNotFound:
            unity = Unity.get_or_404(slug=slug)
            currentUser = User.get(email=current_user.email)
            if (unity.postType == 'draft' and
                    unity.author != currentUser and
                    currentUser.is_admin() is False):
                flash('You must be draft author or admin to view.')
                return redirect(url_for('.listUnity'))
            else:
                form = CommentForm()
                return render_template('unity/staticUnity.html',
                                       pageTitle=unity.title,
                                       unity=unity,
                                       form=form)
