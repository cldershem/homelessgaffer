from flask import (Blueprint, render_template, flash, request,
                   redirect, url_for)
from jinja2 import Markup, TemplateNotFound
from app.models import Page, User
from app.forms import PageForm
from app.constants import DATE_TIME_NOW
from app.utils import makeSlug
from flask.ext.login import login_required, current_user

mod = Blueprint('static_page', __name__, url_prefix='/page')


@mod.route('/')
@mod.route('/listpages')
def listPages():
    pages = Page.objects.all()
    return render_template('page/listPages.html',
                           page="listpages",
                           pages=pages)


@mod.route('/<slug>')
def staticPage(slug):
    try:
        return render_template('page/%s.html' % slug,
                               page=slug)
    except TemplateNotFound:
        page = Page.objects.get_or_404(slug=slug)
        content = Markup(page.content)
        return render_template('page/staticpage.html',
                               title=page.title,
                               slug=page.slug,
                               content=content)


@mod.route('/newpage', methods=['GET', 'POST'])
@login_required
def newPage():
    form = PageForm()

    if request.method == 'POST':
        slug = makeSlug(form.title.data)
        if form.validate() is False:
            return render_template("page/newPage.html", form=form)
        else:
            # if isDraft:
                # do this
            # if isBlogPost:
                # do this
            newPage = Page(title=form.title.data,
                           slug=slug, content=form.content.data)
            newPage.author = User.objects.get(email=current_user.email)
            newPage.save()
            flash('Your page has been posted')
            return redirect(url_for('.staticPage', slug=slug))
    elif request.method == 'GET':
        return render_template("page/newPage.html", form=form, page="newpage")


@mod.route('/<slug>/edit', methods=['GET', 'POST'])
@login_required
def editPage(slug):
    page = Page.objects.get(slug=slug)
    slug = page.slug
    form = PageForm(obj=page)

    if request.method == 'POST':
        if form.validate() is False:
            return render_template('page/editPage.html', title=page.title,
                                   slug=slug, form=form)
        else:
            form.populate_obj(page)
            page.edited_on.append(DATE_TIME_NOW)
            page.save()
            flash("Your page has been updated.")
            return redirect(url_for('.staticPage', slug=slug))
    elif request.method == 'GET':
        form.populate_obj(page)
        return render_template('page/editPage.html', title=page.title,
                               slug=slug, form=form)


@mod.route('/food')  # is food part of posts/blog now?
def food():
    return redirect(url_for('blog.listPosts', tag="food"))
