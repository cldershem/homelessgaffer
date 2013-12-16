from flask.ext.admin import (Admin, BaseView, expose)
from app import app
from flask.ext.admin.contrib.mongoengine import ModelView
from app.models import User, Unity
from wtforms import PasswordField
from flask import flash
from app.constants import DATE_TIME_NOW
from flask.ext.login import current_user


class AdminView(BaseView):

    @expose('/')
    def index(self):
        return self.render('index.html')


class AuthView(ModelView):

    def is_accessible(self):
        if current_user.is_authenticated():
            if current_user.is_admin():
                return True
            # else:
                # flash('You must have admin privlidges to access this page.')
        # else:
            # flash('You must be logged into to do access the admin panel.')
        # return redirect(url_for('users.login'))


class UserView(AuthView):

    column_filters = ('firstname', 'lastname', 'email', 'created_at',
                      'last_seen')
    #form_excluded_columns = ('pwdhash')
    #form_columns = ('firstname', 'lastname', 'email', 'roles')
    column_exclude_list = ('pwdhash')
    column_list = ('firstname', 'lastname', 'email', 'created_at',
                   'last_seen')
    #column_default_sort = 'created_at'

    def scaffold_form(self):
        form_class = super(UserView, self).scaffold_form()
        form_class.password = PasswordField('New password')
        form_class.confirmPassword = PasswordField('Confirm password')
        return form_class

    def on_model_change(self, form, model):
        if model.password or model.confirmPassword:
            if model.password == model.confirmPassword:
                User.set_password(model, model.password)
            else:
                flash("Password and confirm password do not match.")


class UnityView(AuthView):

    def on_model_change(self, form, model):
        model.edited_on.append(DATE_TIME_NOW)


admin = Admin(app)

admin.add_view(UserView(User))
admin.add_view(UnityView(Unity))
