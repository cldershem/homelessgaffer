from flask import (render_template)
from app import app
from app.page.views import mod as staticPageModule
from app.blog.views import mod as blogModule
from app.users.views import mod as usersModule


@app.route('/')
@app.route('/root')
@app.route('/index')
def index():
    return render_template("index.html")


app.register_blueprint(staticPageModule)
app.register_blueprint(blogModule)
app.register_blueprint(usersModule)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("error404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("error500.html"), 500
