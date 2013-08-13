from flask import render_template, url_for, request, redirect, flash, session
from app import app
from forms import LoginForm, RegisterUser

@app.route('/')
@app.route('/root')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/food')
def food():
    return render_template("food.html")

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

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for ' + form.username.data)
        #session['user_id'] = form.user.id
        return redirect('/index')
    return render_template("login.html",
                            form = form)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterUser()
    if form.validate_on_submit():
        flash('Registration requested for ' + form.email.data)
        #session['user_id'] = form.user.id
        return redirect('/index')
    return render_template("register.html",
                            form = form)

@app.route('/logout')
def logout():
    return redirect('/index')
    
@app.errorhandler(404)
def internal_error(error):
    return render_template("error404.html"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template("error500.html"), 500
