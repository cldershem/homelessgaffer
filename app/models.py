from flask import url_for
from app import db, bcrypt
from app.constants import DATE_TIME_NOW


class User(db.Document):

    class Roles(db.EmbeddedDocument):
        can_login = db.BooleanField(default=False)
        can_comment = db.BooleanField(default=True)
        can_post = db.BooleanField(default=True)
        is_admin = db.BooleanField(default=False)

    created_at = db.DateTimeField(required=True, default=DATE_TIME_NOW)
    last_seen = db.DateTimeField(required=True, default=DATE_TIME_NOW)
    firstname = db.StringField(required=True, max_length=64)
    lastname = db.StringField(required=True, max_length=100)
    email = db.StringField(max_length=120, unique=True)
    pwdhash = db.StringField(required=True)
    confirmed = db.DateTimeField(default=None)
    roles = db.EmbeddedDocumentField(Roles, default=Roles)

    def set_password(self, password):
        self.pwdhash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.pwdhash, password)

    def is_authenticated(self):
        return True

    def activate_user(self):
        self.confirmed = DATE_TIME_NOW
        self.roles.can_login = True

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

    def is_admin(self):
        return self.roles.is_admin


class Comment(db.EmbeddedDocument):

    created_at = db.DateTimeField(default=DATE_TIME_NOW, required=True)
    body = db.StringField(required=True)
    author = db.ReferenceField(User)

    def __repr__(self):
        return '<Post %r>' % (self.author)


class Unity(db.Document):

    created_at = db.DateTimeField(default=DATE_TIME_NOW, required=True)
    edited_on = db.ListField(db.DateTimeField(default=DATE_TIME_NOW))
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True)
    author = db.ReferenceField(User)
    body = db.StringField(required=True)
    summary = db.StringField(max_length=255)
    tags = db.ListField(db.StringField(max_length=50))
    source = db.ListField(db.StringField(max_length=255))
    postType = db.StringField(max_length=20, required=True)  # required?
    comments = db.ListField(db.EmbeddedDocumentField(Comment))

    def get_absolute_url(self):
        return url_for('unity', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.title

    meta = {'allow_inheritance': True,
            'indexes': ['-created_at', 'slug'],
            'ordering': ['-created_at']}

    def __repr__(self):
        return '<Unity %r, -%r>' % (self.slug, self.author)
