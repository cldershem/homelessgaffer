from flask import (Blueprint, render_template, url_for, request,
                   redirect, flash, g, abort)
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
    page = "login"

    if request.method == 'POST':
        if form.validate() is False:
            return render_template('users/login.html',
                                   form=form,
                                   page=page)
        else:
            user = User.objects.get(email=form.email.data.lower())
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
                                       page=page)
    elif request.method == 'GET':
        if request.args.get('next'):
            session['next'] = (request.args.get('next') or
                               request.referrer or None)
        return render_template('users/login.html',
                               form=form,
                               page=page)


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
#    form = RegisterUser()
#    page = "register"
#
#    if request.method == 'POST':
#        if form.validate() is False:
#            return render_template('users/register.html',
#                                   form=form,
#                                   page=page)
#        else:
#            newUser = User(firstname=form.firstname.data.title(),
#                           lastname=form.lastname.data.title(),
#                           email=form.email.data.lower())
#            newUser.set_password(form.password.data)
#            newUser.save()
#            payload = get_activation_link(newUser)
#            email_confirmation(newUser, payload)
#            flash("Please confirm your email address.")
#            return redirect(url_for('index'))
#
#    elif request.method == 'GET':
#        return render_template('users/register.html',
#                               form=form,
#                               page=page)

    flash("This feature is currently disabled.")
    return redirect(url_for('index'))


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
#    form = ForgotPasswordForm()
#    page = "forgot password"
#
#    if request.method == 'POST':
#        if not form.validate():
#            return render_template('users/forgotPassword.html',
#                                   form=form,
#                                   page=page)
#        else:
#            try:
#                user = User.objects.get(email=form.email.data)
#            except:
#                flash("That email does not exist, please try another.")
#                return render_template('users/forgotPassword.html',
#                                       form=form,
#                                       page=page)
#            payload = get_password_reset_link(user)
#            email_password_reset(user, payload)
#            flash("Password reset email has been sent. \
#                   Link is good for 24 hours.")
#            return redirect(url_for('index'))
#    elif request.method == 'GET':
#        return render_template('users/forgotPassword.html',
#                               form=form,
#                               page=page)
    flash("This feature is currently disabled.")
    return redirect(url_for('index'))


@mod.route('/resetpassword/<payload>', methods=['GET', 'POST'])
@anon_required
def reset_password(payload):
#    form = ResetPasswordForm()
#    user_email = check_password_reset_link(payload)
#    page = "reset password"
#
#    if not user_email:
#        flash("Token incorrect or has expired.  Please try again.")
#        return redirect(url_for('.forgotPassword'))
#
#    if request.method == 'POST':
#        if not form.validate():
#            return render_template('users/resetPassword.html',
#                                   form=form,
#                                   page=page)
#        else:
#            user = User.objects.get(email=user_email)
#            user.set_password(form.password.data)
#            user.save()
#            #email password reset
#            flash("Password has been reset, please login")
#            return redirect(url_for('.login'))
#    elif request.method == 'GET':
#        return render_template('users/resetPassword.html',
#                               form=form,
#                               page=page)
    flash("This feature is currently disabled.")
    return redirect(url_for('index'))


@mod.route('/profile/<user_id>')
def profile(user_id):
    user = User.objects.get(email=user_id)
    return render_template('users/profile.html',
                           user=user,
                           page=user_id)


############  FACEBOOK  ############
from config import FACEBOOK_CONSUMER_KEY, FACEBOOK_CONSUMER_SECRET
from app import oauth
from flask import session


facebook = oauth.remote_app(
    'facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_CONSUMER_KEY,
    consumer_secret=FACEBOOK_CONSUMER_SECRET,
    request_token_params={'scope': 'email'}
    )


@mod.route('/login/facebook')
def facebookLogin():
#    callback = url_for('.facebook_authorized', _external=True)
#    return facebook.authorize(callback=callback)
    flash("This feature is currently disabled.")
    return redirect(url_for('index'))


def createFBUser(me):
    newUser = User(firstname=me.data['first_name'],
                   lastname=me.data['last_name'],
                   email=me.data['email'])
    newUser.set_password("None")
    newUser.activate_user()
    newUser.save()


@mod.route('/login/facebook/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
            )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    user = User.objects.get(email=me.data['email'])
    if not user:
        createFBUser(me)
    login_user(user)
    next_url = (session.get('next') or
                url_for('.profile', user_id=user.get_id()))
    if session.get('next'):
        session.pop('next')
    return redirect(next_url)


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


###################  GOOGLE  ###########
from config import GOOGLE_CONSUMER_KEY, GOOGLE_CONSUMER_SECRET
from oauth2client.client import (OAuth2WebServerFlow, FlowExchangeError)
import httplib2


flow = OAuth2WebServerFlow(
    client_id=GOOGLE_CONSUMER_KEY,
    client_secret=GOOGLE_CONSUMER_SECRET,
    scope='https://www.googleapis.com/auth/plus.login',
    redirect_uri='http://localhost:5000/users/login/google/authorized')


@mod.route('login/google')
def googleLogin():
#    auth_uri = flow.step1_get_authorize_url()
#    return redirect(auth_uri)
    flash("This feature is currently disabled.")
    return redirect(url_for('index'))


@mod.route('/login/google/authorized')
def googleAuthorized():
    code = request.args.get('code')
    try:
        credentials = flow.step2_exchange(code)
    except FlowExchangeError:
        return "FlowExchangeError"
    gplus_id = credentials.id_token['sub']

    stored_credentials = session.get('credentials')
    stored_gplus_id = session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        flash("Current user is already connected.")
        return redirect(url_for('index'))
    session['credentials'] = credentials.to_json()
    session['gplus_id'] = gplus_id
    flash("Successfully connected user.")
    return redirect(url_for('index'))


@mod.route('/login/google/disconnect')
def googleDisconnect():
    """Revoke current user's tokena nd reset their session."""
    # Only disconnect a connected user.
    credentials = session.get('credentials').to_json()
    if credentials is None:
        flash("User was not connected to Google.")
        return False

    # Execute HTTP GET request to revoke current token.
    access_token = session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%r' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's session.
        del session['credentials']
        return True
    else:
        return False
