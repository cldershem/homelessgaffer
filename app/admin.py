from flask.ext.admin import (Admin, BaseView, expose)
from app import app
from flask.ext.admin.contrib.mongoengine import ModelView
from models import User, Page, Post
#from utils import CKTextAreaField
from wtforms import PasswordField


class AdminView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')


class UserView(ModelView):
    column_filters = ('firstname', 'lastname', 'email', 'created_at',
                      'last_seen')
    column_sortable_list = ('firstname', 'lastname', 'email', 'created_at',
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


class PostView(ModelView):
    column_filters = ['title']
    form_subdocuments = {'comments': {}}


class PageView(ModelView):
    column_filters = ['title']

    #form_overrides = dict(content=CKTextAreaField)
    #create_template = 'admin/edit.html'
    #edit_template = 'admin/edit.html'


admin = Admin(app)

admin.add_view(UserView(User))
admin.add_view(PostView(Post))
admin.add_view(PageView(Page))
