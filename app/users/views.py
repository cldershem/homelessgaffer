from flask import (Blueprint, render_template, url_for, request,
                   redirect, flash, g, abort, session)
from app import lm
from app.forms import (LoginForm, RegisterUser,
                       ForgotPasswordForm, ResetPasswordForm)
from app.models import (User)
from flask.ext.login import (login_user, logout_user,
                             current_user, login_required)
from app.utils import (get_activation_link, check_activation_link,
                       get_password_reset_link, check_password_reset_link)
from app.constants import DATE_TIME_NOW
from app.emails import email_confirmation, email_password_reset
from app.decorators import anon_required


mod = Blueprint('users', __name__, url_prefix='/users')


@lm.user_loader
def load_user(id):
    user = User.objects.get(email=id)
    return user


@mod.before_request
def before_request():
    g.user = current_user


@mod.route('/login', methods=['GET', 'POST'])
@anon_required
def login():
    form = LoginForm()
    pageTitle = "login"

    if request.method == 'POST':
        if form.validate() is False:
            return render_template('users/login.html',
                                   form=form,
                                   pageTitle=pageTitle)
        else:
            user = User.objects.get(email=form.email.data.lower().strip())
            if user and user.roles.can_login is True:
                #add remember_me
                user.last_seen = DATE_TIME_NOW
                user.save()
                login_user(user)
                return redirect(request.args.get('next') or
                                url_for('.profile',
                                        user_id=user.get_id())
                                )
            else:
                flash("Please confirm your email address.")
                return render_template('users/login.html',
                                       form=form,
                                       pageTitle=pageTitle)
    elif request.method == 'GET':
        if request.args.get('next'):
            session['next'] = (request.args.get('next') or
                               request.referrer or None)
        return render_template('users/login.html',
                               form=form,
                               pageTitle=pageTitle)


def after_login(resp):
    pass


@mod.route('/logout')
@login_required
def logout():
    logout_user()
    if session.get('credentials'):
        if redirect(url_for('.googleDisconnect')):
            flash("Successfully disconnected from Google.")
    flash("Successfully logged out.")
    session.clear()
    return redirect(url_for('index'))


@mod.route('/register', methods=['GET', 'POST'])
@anon_required
def register():
    form = RegisterUser()
    pageTitle = "register"

    if request.method == 'POST':
        if form.validate() is False:
            return render_template('users/register.html',
                                   form=form,
                                   pageTitle=pageTitle)
        else:
            newUser = User(firstname=form.firstname.data.title(),
                           lastname=form.lastname.data.title(),
                           email=form.email.data.lower().strip())
            newUser.set_password(form.password.data)
            newUser.save()
            payload = get_activation_link(newUser)
            email_confirmation(newUser, payload)
            flash("Please confirm your email address.")
            return redirect(url_for('index'))

    elif request.method == 'GET':
        return render_template('users/register.html',
                               form=form,
                               pageTitle=pageTitle)

    # flash("This feature is currently disabled.")
    # return redirect(url_for('index'))


@mod.route('/activate/<payload>')
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
        return redirect(url_for('.login'))
    else:
        return abort(404)


@mod.route('/forgotpassword', methods=['GET', 'POST'])
@anon_required
def forgotPassword():
    form = ForgotPasswordForm()
    pageTitle = "forgot password"

    if request.method == 'POST':
        if not form.validate():
            return render_template('users/forgotPassword.html',
                                   form=form,
                                   pageTitle=pageTitle)
        else:
            try:
                user = User.objects.get(email=form.email.data.lower().strip())
            except:
                flash("That email does not exist, please try another.")
                return render_template('users/forgotPassword.html',
                                       form=form,
                                       pageTitle=pageTitle)
            # disallows password reset link to be reused
            oldhash = user.pwdhash[:10]
            payload = get_password_reset_link(user) + oldhash
            email_password_reset(user, payload)

            flash("Password reset email has been sent. \
                   Link is good for 24 hours.")
            return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('users/forgotPassword.html',
                               form=form,
                               pageTitle="Forgot Password")


@mod.route('/resetpassword/<payload>', methods=['GET', 'POST'])
@anon_required
def reset_password(payload):
    form = ResetPasswordForm()
    pageTitle = "reset password"

    # disallows password reset link to be reused
    oldhash = payload[len(payload)-10:len(payload)]
    payload = payload[:len(payload)-10]

    user_email = check_password_reset_link(payload)

    if user_email:
        user_oldhash = User.objects.get(email=user_email).pwdhash[:10]
        if oldhash != user_oldhash:
            flash("Token has been used previously.  Please try again.")
            return redirect(url_for('.forgotPassword'))

    if not user_email:
        flash("Token incorrect or has expired.  Please try again.")
        return redirect(url_for('.forgotPassword'))

    if request.method == 'POST':
        if not form.validate():
            return render_template('users/resetPassword.html',
                                   form=form,
                                   pageTitle=pageTitle)
        else:
            user = User.objects.get(email=user_email)
            user.set_password(form.password.data)
            user.save()
            #email password reset
            flash("Password has been reset, please login")
            return redirect(url_for('.login'))
    elif request.method == 'GET':
        return render_template('users/resetPassword.html',
                               form=form,
                               pageTitle=pageTitle)


@mod.route('/profile/<user_id>')
def profile(user_id):
    user = User.objects.get(email=user_id)
    return render_template('users/profile.html',
                           user=user,
                           pageTitle=user_id)
