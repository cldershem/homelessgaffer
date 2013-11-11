from flask import (Blueprint, render_template, flash, request,
                   redirect, url_for)
# from jinja2 import TemplateNotFound
from app.models import Unity, User  # , Comment
from app.forms import UnityForm
# from app.constants import DATE_TIME_NOW
from app.utils import makeSlug, markRight
from flask.ext.login import login_required, current_user
# from flask.ext.mongoengine import Pagination
# from app import app

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


@mod.route('/newunity', methods=['GET', 'POST'])
@login_required
def newUnity():
    form = UnityForm()

    if request.method == 'Post':
        slug = makeSlug(form.title.data)
        if not form.validate():
            return render_template("unity/newUnity.html", form=form)
        else:
            # if form.isDraft.data:
                # save as form.title.data + "-draft"
            # elif !form.isDraft.data:
                # save as draft?
                # send to preview confirm page
                    # if confirm
                        # remove "draft" indicator
                        # publish
                    # else:
                        # redirect to edit page
                        # flash "edit or save as draft"
            # if isBlogPost:
                # do this
            newUnity = Unity(title=form.title.data,
                             slug=slug,
                             body=form.body.data)
            if form.tags.data:
                newUnity.tags = form.tags.data.split(', ')
            if form.source.data:
                newUnity.source = form.source.data.split(', ')
            newUnity.author = User.objects.get(email=current_user.email)
            newUnity.save()
            flash('Your unity has been posted.')
            return redirect(url_for('.staticUnity', slug=slug))
    elif request.method == 'GET':
        return render_template("unity/newUnity.html",
                               form=form,
                               page="newUnity")


@mod.route('/<slug>')
def staticUnity(slug):
    unity = Unity.objects.get_or_404(slug=slug)
    body = markRight(unity.body)
    return render_template(
        'unity/staticUnity.html',
        pageTitle=unity.title,
        slug=unity.slug,
        body=body)
