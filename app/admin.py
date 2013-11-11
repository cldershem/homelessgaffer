from flask.ext.admin import (Admin, BaseView, expose)
from app import app
from flask.ext.admin.contrib.mongoengine import ModelView
from models import User, Page, Post, Unity
#from utils import CKTextAreaField
from wtforms import PasswordField
from flask import flash
from app.constants import DATE_TIME_NOW
# from app.decorators import admin_required


class AdminView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')


class UserView(ModelView):
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


class PostView(ModelView):
    column_filters = ['title']
    column_exclude_list = ['body']
    form_excluded_columns = ['created_at']
    form_subdocuments = {'comments': {}}

    def on_model_change(self, form, model):
        model.edited_on.append(DATE_TIME_NOW)


class PageView(ModelView):
    column_filters = ['title', 'slug', 'created_at']

    #form_overrides = dict(content=CKTextAreaField)
    #create_template = 'admin/edit.html'
    #edit_template = 'admin/edit.html'

    def on_model_change(self, form, model):
        model.edited_on.append(DATE_TIME_NOW)


class UnityView(ModelView):

    def on_model_change(self, form, model):
        model.edited_on.append(DATE_TIME_NOW)


admin = Admin(app)

admin.add_view(UserView(User))
admin.add_view(PostView(Post))
admin.add_view(PageView(Page))
admin.add_view(UnityView(Unity))
