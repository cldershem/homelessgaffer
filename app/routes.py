from flask import (render_template, url_for, request, redirect, flash,
                   g, abort)
from app import app, lm
from forms import LoginForm, RegisterUser, CommentForm, PostForm, PageForm
from jinja2 import Markup
from models import (User, Post, Comment, Page)
from flask.ext.login import (login_user, logout_user,
                             current_user, login_required)
from utils import makeSlug, get_activation_link, check_activation_link
from flask.ext.mongoengine import Pagination
from app.constants import DATE_TIME_NOW
from emails import email_confirmation


@lm.user_loader
def load_user(id):
    user = User.objects.get(email=id)
    return user


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/root')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/food')
def food():
    return redirect(url_for('listPosts', tag="food"))


@app.route('/bike')
def bike():
    return render_template("bike.html")


@app.route('/work')
def work():
    return render_template("work.html")


@app.route('/resume')
def resume():
    return render_template("resume.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/dev')
def dev():
    return render_template("dev.html")


@app.route('/battleship')
def battleship():
    return render_template("battleship.html")


@app.route('/page/<slug>')
def staticPage(slug):
    page = Page.objects.get_or_404(slug=slug)
    content = Markup(page.content)
    return render_template('staticpage.html', title=page.title,
                           slug=page.slug, content=content)


@app.route('/page/newpage', methods=['GET', 'POST'])
@login_required
def newPage():
    form = PageForm()

    if request.method == 'POST':
        slug = makeSlug(form.title.data)
        if form.validate() is False:
            return render_template("newPage.html", form=form)
        else:
            newPage = Page(title=form.title.data,
                           slug=slug, content=form.content.data)
            newPage.author = User.objects.get(email=current_user.email)
            newPage.save()
            flash('Your page has been posted')
            return redirect(url_for('staticPage', slug=slug))
    elif request.method == 'GET':
        return render_template("newPage.html", form=form)


@app.route('/page/<slug>/edit', methods=['GET', 'POST'])
@login_required
def editPage(slug):
    page = Page.objects.get(slug=slug)
    slug = page.slug
    form = PageForm(obj=page)

    if request.method == 'POST':
        if form.validate() is False:
            return render_template('editPage.html', title=page.title,
                                   slug=slug, form=form)
        else:
            form.populate_obj(page)
            page.edited_on.append(DATE_TIME_NOW)
            page.save()
            flash("Your page has been updated.")
            return redirect(url_for('staticPage', slug=slug))
    elif request.method == 'GET':
        form.populate_obj(page)
        return render_template('editPage.html', title=page.title,
                               slug=slug, form=form)


@app.route('/page/listpages')
def listPages():
    pages = Page.objects.all()
    return render_template('listPages.html', pages=pages)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated() is True:
        return redirect(url_for('index'))

    if request.method == 'POST':
        if form.validate() is False:
            return render_template('login.html', form=form)
        else:
            user = User.objects.get(email=form.email.data.lower())
            if user and user.roles.can_login is True:
                #add remember_me
                user.last_seen = DATE_TIME_NOW
                user.save()
                login_user(user)
                return redirect(request.args.get('next') or
                                url_for('profile', user=current_user.email))
            else:
                flash("Please confirm your email address.")
                return render_template('login.html', form=form)
    elif request.method == 'GET':
        return render_template('login.html', form=form)


def after_login(resp):
    pass


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterUser()
    if current_user.is_authenticated() is True:
        flash("You are already a user.")
        return redirect(url_for('index'))

    if request.method == 'POST':
        if form.validate() is False:
            return render_template('register.html', form=form)
        else:
            newUser = User(firstname=form.firstname.data.title(),
                           lastname=form.lastname.data.title(),
                           email=form.email.data.lower())
            newUser.set_password(form.password.data)
            newUser.save()
            payload = get_activation_link(newUser)
            email_confirmation(newUser, payload)
            flash("Please confirm your email address.")
            return redirect(url_for('index'))

    elif request.method == 'GET':
        return render_template('register.html', form=form)


@app.route('/user/activate/<payload>')
def activateUser(payload):
    user_email = check_activation_link(payload)
    if not user_email:
        return abort(404)
    user = User.objects.get(email=user_email)
    if user:
        if user.confirmed is None:
            user.activate_user()
            user.save()
            flash('Your account has been activated.')
        else:
            flash('Your account was already active.')
        return redirect(url_for('login'))
    else:
        return abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("error500.html"), 500


@app.route('/profile/<user>')
def profile(user):
    last_seen = User.objects.get(email=user).last_seen
    return render_template('/profile.html', user=user, last_seen=last_seen)


@app.route('/blog/newpost', methods=['GET', 'POST'])
@login_required
def newPost():
    form = PostForm()

    if request.method == 'POST':
        if form.validate() is False:
            return render_template("newPost.html", form=form)
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
        return render_template("newPost.html", form=form)


@app.route('/blog/listposts',
           defaults={'tag': None,
                     'user': None,
                     'page': 1})
@app.route('/blog/listposts/page/<int:page>',
           defaults={'tag': None,
                     'user': None})
@app.route('/blog/listposts/tag/<tag>',
           defaults={'user': None,
                     'page': 1})
@app.route('/blog/listposts/tag/<tag>/page/<int:page>',
           defaults={'user': None})
@app.route('/blog/listposts/user/<user>',
           defaults={'tag': None,
                     'page': 1})
@app.route('/blog/listposts/user/<user>/page/<int:page>',
           defaults={'tag': None})
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
    return render_template('listPosts.html',
                           posts=posts, title=title, page=page)


@app.route('/blog/<slug>', methods=['GET', 'POST'])
def singlePost(slug):
    form = CommentForm()
    post = Post.objects.get_or_404(slug=slug)

    if request.method == 'POST':
        if form.validate() is False:
            return render_template('singlePost.html', post=post, form=form)
        else:
            newComment = Comment(body=form.comment.data)
            newComment.author = User.objects.get(email=current_user.email)
            post.comments.append(newComment)
            post.save()
            form.comment.data = None  # resets field to empty on refresh
            flash('Comment Posted')
        return render_template('singlePost.html', post=post, form=form)
    elif request.method == 'GET':
        return render_template('singlePost.html', post=post, form=form)
