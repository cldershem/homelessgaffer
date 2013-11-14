from flask import (Blueprint, render_template, flash, request,
                   redirect, url_for)
from jinja2 import TemplateNotFound
from app.models import Unity, User, Comment
from app.forms import UnityForm, CommentForm
from app.constants import DATE_TIME_NOW
from app.utils import makeSlug, markRight
from flask.ext.login import login_required, current_user
from flask.ext.mongoengine import Pagination

mod = Blueprint('unity', __name__, url_prefix='/unity')


@mod.route('/', defaults={'tag': None, 'user': None, 'pageNum': 1})
@mod.route('/listposts', defaults={'tag': None, 'user': None, 'pageNum': 1})
@mod.route('/listposts/page/<int:pageNum>',
           defaults={'tag': None, 'user': None})
@mod.route('/listposts/tag/<tag>', defaults={'user': None, 'pageNum': 1})
@mod.route('/listposts/tag/<tag>/page/<int:pageNum>', defaults={'user': None})
@mod.route('/listposts/user/<user>', defaults={'tag': None, 'pageNum': 1})
@mod.route('/listposts/user/<user>/page/<int:pageNum>', defaults={'tag': None})
def listUnity(tag, user, pageNum):
    # if postToBlog:
    #     display list with preview
    # if !postToBlog:
    #     display list of titles in order of recently edited
    # if !draft:
    #     display list of non drafts
    # if tag or if user:
    #     display list of both
    if tag:
        unitySet = Pagination(Unity.objects(tags=tag), pageNum, 10)
        pageTitle = tag
    if user:
        user = User.objects.get(email=user)
        unitySet = Pagination(Unity.objects(author=user), pageNum, 10)
        pageTitle = user.email
    elif not tag and not user:
        unitySet = Pagination(Unity.objects.all(), pageNum, 10)
        pageTitle = "listUnity"
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
            return render_template("unity/newUnity.html", form=form)
        else:
            slug = makeSlug(form.title.data)
            # if form.isDraft.data:
            #     save as form.title.data + "-draft"
            # elif !form.isDraft.data:
            #     save as draft?
            #     send to preview confirm page
            #         if confirm
            #             remove "draft" indicator
            #             publish
            #         else:
            #             redirect to edit page
            #             flash "edit or save as draft"
            # if isBlogPost:
            #     do this
            newUnity = Unity(title=form.title.data,
                             slug=slug,
                             body=form.body.data)
            if form.tags.data:
                newUnity.tags = form.tags.data
            if form.source.data:
                newUnity.source = form.tags.data
            newUnity.author = User.objects.get(email=current_user.email)
            newUnity.save()
            flash('Your unity has been posted.')
            return redirect(url_for('.staticUnity', slug=slug))
    elif request.method == 'GET':
        return render_template("unity/newUnity.html",
                               form=form,
                               page="newUnity")


@mod.route('/<slug>/edit', methods=['GET', 'POST'])
@login_required
def editUnity(slug):
    unity = Unity.objects.get(slug=slug)
    slug = unity.slug
    form = UnityForm(obj=unity)

    def validate_on_update():
        if slug == makeSlug(form.title.data):
            return form.validate()
        else:
            return form.validate_with_slug()

    if request.method == 'POST':
        if not validate_on_update():
            return render_template('unity/newUnity.html',
                                   title=unity.title,
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


@mod.route('/<slug>')
def staticUnity(slug):
    unity = Unity.objects.get_or_404(slug=slug)
    body = markRight(unity.body)
    form = CommentForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('unity/staticUnity.html',
                                   unity=unity,
                                   form=form)
        else:
            newComment = Comment(body=form.comment.data)
            newComment.author = User.objects.get(email=current_user.email)
            unity.comments.append(newComment)
            unity.save()
            form.comment.data = None  # resets field on refresh
            flash('Comment Posted')
        return render_template('unity/staticUnity.html',
                               unity=unity,
                               form=form)
    elif request.method == 'GET':
        try:
            return render_template('unity/%s.html' % slug,
                                   pageTitle=slug)
        except TemplateNotFound:
            return render_template('unity/staticUnity.html',
                                   pageTitle=unity.title,
                                   slug=unity.slug,
                                   body=body,
                                   form=form)
