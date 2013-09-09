from flask import (Blueprint, request, redirect, url_for, render_template,
                   flash)
from app.models import Post, Comment, User
from app.forms import PostForm, CommentForm
from app.utils import makeSlug
from flask.ext.login import login_required, current_user
from flask.ext.mongoengine import Pagination

mod = Blueprint('blog', __name__, url_prefix='/blog')


@mod.route('/newpost', methods=['GET', 'POST'])
@login_required
def newPost():
    form = PostForm()

    if request.method == 'POST':
        if form.validate() is False:
            return render_template("blog/newPost.html", form=form)
        else:
            slug = makeSlug(form.title.data)
            newPost = Post(title=form.title.data, slug=slug,
                           body=form.body.data)
            if form.tags.data:
                newPost.tags = form.tags.data.split(', ')
            newPost.author = User.objects.get(email=current_user.email)
            newPost.save()
            flash('Your post has been posted.')
            return redirect(url_for('singlePost', slug=slug))

    elif request.method == 'GET':
        return render_template("blog/newPost.html", form=form)


@mod.route('/', defaults={'tag': None,
                          'user': None,
                          'page': 1})
@mod.route('/listposts', defaults={'tag': None,
                                   'user': None,
                                   'page': 1})
@mod.route('/listposts/page/<int:page>', defaults={'tag': None,
                                                   'user': None})
@mod.route('/listposts/tag/<tag>', defaults={'user': None,
                                             'page': 1})
@mod.route('/listposts/tag/<tag>/page/<int:page>', defaults={'user': None})
@mod.route('/listposts/user/<user>', defaults={'tag': None,
                                               'page': 1})
@mod.route('/listposts/user/<user>/page/<int:page>', defaults={'tag': None})
def listPosts(tag, user, page):
    if tag:
        paginator = Pagination(Post.objects(tags=tag), page, 10)
        posts = paginator
        title = tag
    if user:
        user = User.objects.get(email=user)
        paginator = Pagination(Post.objects(author=user), page, 10)
        posts = paginator
        title = user.email
    elif tag is None and user is None:
        paginator = Pagination(Post.objects.all(), page, 10)
        posts = paginator
        title = "listposts"
    return render_template('blog/listPosts.html',
                           posts=posts, title=title, page=page)


@mod.route('/<slug>', methods=['GET', 'POST'])
def singlePost(slug):
    form = CommentForm()
    post = Post.objects.get_or_404(slug=slug)

    if request.method == 'POST':
        if form.validate() is False:
            return render_template('blog/singlePost.html',
                                   post=post,
                                   form=form)
        else:
            newComment = Comment(body=form.comment.data)
            newComment.author = User.objects.get(email=current_user.email)
            post.comments.append(newComment)
            post.save()
            form.comment.data = None  # resets field to empty on refresh
            flash('Comment Posted')
        return render_template('blog/singlePost.html', post=post, form=form)
    elif request.method == 'GET':
        return render_template('blog/singlePost.html', post=post, form=form)
