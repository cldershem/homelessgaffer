from flask import Blueprint, render_template, abort
from jinja2 import Markup, TemplateNotFound
from app.models import Page


static_page = Blueprint('static_page', __name__,
                        template_folder='templates')


@static_page.route('/')  # , defaults={'page': 'listpages'})
@static_page.route('/<page>')
def showStaticPage(page):
    try:
        return render_template('page/%s.html' % page, page=page)
    except TemplateNotFound:
        abort(404)

#################

#@app.route('/page/food')
#def food():
#    return redirect(url_for('listPosts', tag="food"))


#@app.route('/page/bike')
#def bike():
#    return render_template("bike.html")


#@app.route('/page/work')
#def work():
#    return render_template("work.html")


#@app.route('/page/resume')
#def resume():
#    return render_template("resume.html")


#@app.route('/page/about')
#def about():
#    return render_template("about.html")


#@app.route('/page/contact')
#def contact():
#    return render_template("contact.html")


#@app.route('/page/dev')
#def dev():
#    return render_template("dev.html")


#@app.route('/page/battleship')
#def battleship():
#    return render_template("battleship.html")

#~ @app.route('/page/newpage', methods=['GET', 'POST'])
#~ @login_required
#~ def newPage():
    #~ form = PageForm()
#~
    #~ if request.method == 'POST':
        #~ slug = makeSlug(form.title.data)
        #~ if form.validate() is False:
            #~ return render_template("newPage.html", form=form)
        #~ else:
            #~ newPage = Page(title=form.title.data,
                           #~ slug=slug, content=form.content.data)
            #~ newPage.author = User.objects.get(email=current_user.email)
            #~ newPage.save()
            #~ flash('Your page has been posted')
            #~ return redirect(url_for('staticPage', slug=slug))
    #~ elif request.method == 'GET':
        #~ return render_template("newPage.html", form=form)
#~
#~
#~ @app.route('/page/<slug>/edit', methods=['GET', 'POST'])
#~ @login_required
#~ def editPage(slug):
    #~ page = Page.objects.get(slug=slug)
    #~ slug = page.slug
    #~ form = PageForm(obj=page)
#~
    #~ if request.method == 'POST':
        #~ if form.validate() is False:
            #~ return render_template('editPage.html', title=page.title,
                                   #~ slug=slug, form=form)
        #~ else:
            #~ form.populate_obj(page)
            #~ page.edited_on.append(DATE_TIME_NOW)
            #~ page.save()
            #~ flash("Your page has been updated.")
            #~ return redirect(url_for('staticPage', slug=slug))
    #~ elif request.method == 'GET':
        #~ form.populate_obj(page)
        #~ return render_template('editPage.html', title=page.title,
                               #~ slug=slug, form=form)
#~
#~

#####

semi_static_page = Blueprint('semi_static_page', __name__,
                             template_folder='templates',
                             url_prefix='/page')


@semi_static_page.route('/listpages')
def listPages():
    pages = Page.objects.all()
    return render_template('page/listPages.html', pages=pages)


@semi_static_page.route('/<slug>')
def showSemiStaticPage(slug):
    page = Page.objects.get_or_404(slug=slug)
    content = Markup(page.content)
    return render_template('page/staticpage.html', title=page.title,
                           slug=page.slug, content=content)
