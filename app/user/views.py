from flask import (render_template, url_for, request, redirect, flash,
                   g, abort)
from app import app, lm
from forms import (LoginForm, RegisterUser,
                   ForgotPasswordForm, ResetPasswordForm)
from models import (User)
from flask.ext.login import (login_user, logout_user,
                             current_user, login_required)
from utils import (get_activation_link, check_activation_link,
                   get_password_reset_link, check_password_reset_link)
from app.constants import DATE_TIME_NOW
from emails import email_confirmation, email_password_reset
from decorators import anon_required
from app.page.views import mod as staticPage
from app.blog.views import mod as blogPost


@lm.user_loader
def load_user(id):
    user = User.objects.get(email=id)
    return user


@app.before_request
def before_request():
    g.user = current_user


# user


@app.route('/login', methods=['GET', 'POST'])
@anon_required
def login():
    form = LoginForm()

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
                                url_for('profile',
                                        user=current_user.email)
                                )
            else:
                flash("Please confirm your email address.")
                return render_template('login.html', form=form)
    elif request.method == 'GET':
        return render_template('login.html', form=form)


def after_login(resp):
    pass


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
@anon_required
def register():
    form = RegisterUser()

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
@anon_required
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


@app.route('/user/forgotpassword', methods=['GET', 'POST'])
@anon_required
def forgotPassword():
    form = ForgotPasswordForm()

    if request.method == 'POST':
        if not form.validate():
            return render_template('forgotPassword.html', form=form)
        else:
            try:
                user = User.objects.get(email=form.email.data)
            except:
                flash("That email does not exist, please try another.")
                return render_template('forgotPassword.html', form=form)
            payload = get_password_reset_link(user)
            email_password_reset(user, payload)
            flash("Password reset email has been sent. \
                   Link is good for 24 hours.")
            return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('forgotPassword.html', form=form)


@app.route('/user/resetpassword/<payload>', methods=['GET', 'POST'])
@anon_required
def reset_password(payload):
    form = ResetPasswordForm()
    user_email = check_password_reset_link(payload)

    if not user_email:
        flash("Token incorrect or has expired.  Please try again.")
        return redirect(url_for('forgotPassword'))

    if request.method == 'POST':
        if not form.validate():
            return render_template('resetPassword.html', form=form)
        else:
            user = User.objects.get(email=user_email)
            user.set_password(form.password.data)
            user.save()
            #email password reset
            flash("Password has been reset, please login")
            return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('resetPassword.html', form=form)


@app.route('/profile/<user>')  # should but /user/profile/<user>
def profile(user):
    last_seen = User.objects.get(email=user).last_seen
    return render_template('/profile.html', user=user, last_seen=last_seen)
#end user
