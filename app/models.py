import datetime
from flask import url_for
from app import db  # app
from werkzeug import generate_password_hash, check_password_hash
#from utils import makeSlug


class User(db.Document):

    class Roles(db.EmbeddedDocument):
        can_login = db.BooleanField(required=True, default=True)
        can_comment = db.BooleanField(required=True, default=True)
        can_post = db.BooleanField(required=True, default=True)
        is_admin = db.BooleanField(required=True, default=False)

    created_at = db.DateTimeField(default=datetime.datetime.now,
                                  required=True)
    last_seen = db.DateTimeField(default=datetime.datetime.now)
    firstname = db.StringField(max_length=64)
    lastname = db.StringField(max_length=100)
    email = db.StringField(max_length=120, unique=True)
    pwdhash = db.StringField()
    roles = db.EmbeddedDocumentField(Roles, default=Roles)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email

    def __repr__(self):
        return '<User %r, %r>' % (self.firstname, self.email)

    def __unicode__(self):
        return self.email


class Comment(db.EmbeddedDocument):

    created_at = db.DateTimeField(default=datetime.datetime.now,
                                  required=True)
    body = db.StringField(required=True)
    author = db.ReferenceField(User)

    def __repr__(self):
        return '<Post %r>' % (self.author)


class Post(db.Document):

    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True)
    author = db.ReferenceField(User)
    body = db.StringField(required=True)
    tags = db.ListField(db.StringField(max_length=50))
    comments = db.ListField(db.EmbeddedDocumentField(Comment))

    def get_absolute_url(self):
        return url_for('post', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.title

    meta = {'allow_inheritance': True,
            'indexes': ['-created_at', 'slug'],
            'ordering': ['-created_at']}

    def __repr__(self):
        return '<Post %r, -%r>' % (self.slug, self.author)


class Page(db.Document):

    created_at = db.DateTimeField(default=datetime.datetime.now,
                                  required=True)
    title = db.StringField(required=True)
    slug = db.StringField(required=True)
    content = db.StringField(required=True)
    author = db.ReferenceField(User)

    meta = {'allow_inheritance': True,
            'indexes': ['-created_at', 'title'],
            'ordering': ['-created_at']}

    def __repr__(self):
        return '<Page %r>' % (self.title)
