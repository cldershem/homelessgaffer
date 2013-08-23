from flask.ext.admin import (Admin, BaseView, expose)
from app import app
from flask.ext.admin.contrib.mongoengine import ModelView
from models import User, Page, Post
#from utils import CKTextAreaField


class AdminView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')


class UserView(ModelView):
    column_filters = ['email']


class PostView(ModelView):
    column_filters = ['title']
    form_subdocuments = {'comments': {}}


class PageView(ModelView):
    column_filters = ['title']

    #form_overrides = dict(content=CKTextAreaField)
    #create_template = 'admin/edit.html'
    #edit_template = 'admin/edit.html'


class CommentView(ModelView):
    pass

admin = Admin(app)

admin.add_view(UserView(User))
admin.add_view(PostView(Post))
admin.add_view(PageView(Page))
