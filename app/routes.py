from flask import (render_template)
from app import app
from app.page.views import mod as staticPageModule
from app.blog.views import mod as blogModule
from app.users.views import mod as usersModule
from app.unity.views import mod as unityModule


@app.route('/')
@app.route('/root')
@app.route('/index')
def index():
    return render_template("index.html", pageTitle="root")


app.register_blueprint(staticPageModule)
app.register_blueprint(blogModule)
app.register_blueprint(usersModule)
app.register_blueprint(unityModule)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error404.html",
                           pageTitle="error404"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("error500.html",
                           pageTitle="error500"), 500
