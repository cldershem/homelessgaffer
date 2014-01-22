"""
    app.models
    ~~~~~~~~~

    All models for db document structure.  Maybe eventually be split into
    separate modules for each blueprint.

    :copyright: and :license: see TOPMATTER.
"""

from flask import url_for
from app import db, bcrypt
from app.constants import DATE_TIME_NOW
from app.utils import get_serializer, get_timed_serializer
from itsdangerous import (BadSignature, SignatureExpired)


class User(db.Document):
    """
    Defines db model for `User`.
    """

    class Roles(db.EmbeddedDocument):
        """
        Doc embedded in User showing users permissions, roles, and rights.
        """
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
        """Takes user password and stores it as a hash using bcrypt."""
        self.pwdhash = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        """Takes a password and checks its bcrypt hash against the db."""
        return bcrypt.check_password_hash(self.pwdhash, password)

    def is_authenticated(self):
        """Returns true if user is logged in."""
        return True

    def activate_user(self):
        """
        Sets user to active, allowing user to login.  Sets `User.confrimed`
        to `DATE_TIME_NOW` and updates `user.roles.can_login` to `True`.
        """
        self.confirmed = DATE_TIME_NOW
        self.roles.can_login = True

    def is_active(self):
        """
        Returns `True` if user is active.  Will be used to find banned,
        suspended, or defunct users in the future.
        """
        return True

    def is_anonymous(self):
        """
        Returns `True` if user is logged in.  Returns `False` if user
        not logged in.
        """
        return False

    def get_id(self):
        """Returns user.email which is currently used as the unique ID."""
        return self.email

    def __repr__(self):
        return '<User %r, %r>' % (self.firstname, self.email)

    def __unicode__(self):
        return self.email

    def is_admin(self):
        """Returns `user.roles.is_admin`."""
        return self.roles.is_admin

    @staticmethod
    def get(**kwargs):
        """returns `User` object."""
        return User.objects.get(**kwargs)

    @staticmethod
    def get_activation_link(user):
        """
        Takes a `user` object and returns their user_id as a url-safe,
        serialized version as `payload`.
        """
        user_id = user.get_id()
        s = get_serializer()
        payload = s.dumps(user_id)
        return payload

    @staticmethod
    def check_activation_link(payload):
        """
        Takes `payload`, checks if valid.  Returns false if invalid, or
        `user_id` if valid.
        """
        s = get_serializer()
        try:
            user_id = s.loads(payload)
        except BadSignature:
            return False
        return user_id

    @staticmethod
    def get_password_reset_link(user):
        """
        Takes a `user` object and using `get_timed_serializer()` returns a
        url-safe, serialized, single-user, payload with a timestamp, which can
        then be used to create a link to reset a users password.
        """
        user_id = user.get_id()
        s = get_timed_serializer()

        # disallows password reset link to be reused
        oldhash = user.pwdhash[:10]
        payload = s.dumps(user_id+oldhash)
        return payload

    @staticmethod
    def check_password_reset_link(payload):
        """
        Takes payload and checks if valid.  Returns `user_id` and `oldhash` if
        valid and False if invalid.
        """
        s = get_timed_serializer()
        try:
            # disallows password reset link to be reused
            unhashed_payload = s.loads(payload, max_age=86400)
            oldhash = unhashed_payload[
                len(unhashed_payload)-10:len(unhashed_payload)]
            user_id = unhashed_payload[:-10]
        except SignatureExpired or BadSignature:
            return False
        return (user_id, oldhash)


class Comment(db.EmbeddedDocument):
    """Defines db model for `Comment`."""

    created_at = db.DateTimeField(default=DATE_TIME_NOW, required=True)
    body = db.StringField(required=True)
    author = db.ReferenceField(User)

    def __repr__(self):
        return '<Post %r>' % (self.author)


class Unity(db.Document):
    """Defines db model for `Unity`."""

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
        """Returns url for individual pages using slug."""
        return url_for('unity', kwargs={"slug": self.slug})

    def __unicode__(self):
        return self.title

    meta = {'allow_inheritance': True,
            'indexes': ['-created_at', 'slug'],
            'ordering': ['-created_at']}

    def __repr__(self):
        return '<Unity %r, -%r>' % (self.slug, self.author)

    @staticmethod
    def get_set(**kwargs):
        """Returns a set of objects."""
        return Unity.objects(**kwargs)

    @staticmethod
    def get(**kwargs):
        """Returns a unique object."""
        return Unity.objects.get(**kwargs)

    @staticmethod
    def get_or_404(**kwargs):
        """Returns a unique object or 404."""
        return Unity.objects.get_or_404(**kwargs)
