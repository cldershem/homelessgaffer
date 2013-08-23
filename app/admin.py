from flask.ext.admin import (Admin, BaseView, AdminIndexView, expose)
from app import app, db
from flask.ext.admin.contrib.mongoengine import ModelView
from models import User, Post, Page
from utils import CKTextAreaField

class AdminView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')

class UserView(ModelView):
    column_filters = ['email']

class PostView(ModelView):
    column_filters = ['title']

class PageView(ModelView):
    column_filters = ['title']    

    #form_overrides = dict(content=CKTextAreaField)
    #create_template = 'admin/edit.html'
    #edit_template = 'admin/edit.html'

admin = Admin(app)

admin.add_view(UserView(User))
admin.add_view(PostView(Post))
admin.add_view(PageView(Page))
