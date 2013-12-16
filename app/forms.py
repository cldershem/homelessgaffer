"""
    app.forms
    ~~~~~~~~~

    All classes for forms needed throughout the application.  May eventually
    be broken out into seperate modules for each blueprint.

    :copyright: and :license: see TOPMATTER.
"""

from flask.ext.wtf import Form, RecaptchaField
from wtforms import (TextField, TextAreaField, PasswordField, SubmitField,
                     BooleanField, SelectField)
from wtforms.validators import Email, EqualTo, Required
from models import User, Unity
from mongoengine.queryset import DoesNotExist
from utils import makeSlug, TagListField
from flask.ext.pagedown.fields import PageDownField


class LoginForm(Form):
    """Class for login form."""

    email = TextField('email', [Required(
                      "Please enter a username.")])
    password = PasswordField('password', [Required(
                             "Please enter a password")])
    remember_me = BooleanField('remember me')
    submit = SubmitField("login")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        """
        Attempts to look up `self.email.data` in db returning an error if not
        found or sending it to `user.check_password()` if found.
        """
        if not Form.validate(self):
            return False
        try:
            user = User.objects.get(email=self.email.data.lower().strip())
        except DoesNotExist:
            self.email.errors.append("Invalid email address")
            return False
        if user and user.check_password(self.password.data):
            return True
        else:
            self.password.errors.append("Invalid password")
            return False


class RegisterUser(Form):
    """Class for registration form."""

    firstname = TextField("First name",  [Required(
                          "Please enter your first name.")])
    lastname = TextField("Last name",  [Required(
                         "Please enter your last name.")])
    email = TextField("Email",
                      [Required("Please enter your email address."),
                       Email("Please engter a valid email address.")])
    password = PasswordField('New Password', [Required(),
                             EqualTo('confirm',
                                     message='Passwords must match')])
    confirm = PasswordField('Confirm', [Required(
                            "Password again, please.")])
    recaptcha = RecaptchaField("reCaptcha")
    submit = SubmitField("Create account")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        """
        Checks if `self.email` alread in db.  Returns error if found or True
        if unique.
        """
        if not Form.validate(self):
            return False
        try:
            user = User.objects.get(email=self.email.data.lower().strip())
            if user:
                self.email.errors.append("That email already exists.")
            return False
        except DoesNotExist:
            return True


class CommentForm(Form):
    """Class for comment form."""

    comment = TextAreaField('comment', [Required()])
    submit = SubmitField("submit")


class ForgotPasswordForm(Form):
    """Class for forgot password form."""

    email = TextField("email", [Required("Please enter your email.")])
    submit = SubmitField("submit")


class ResetPasswordForm(Form):
    """Class for reset password form."""

    password = PasswordField('New Password', [Required(),
                             EqualTo('confirm',
                                     message='Passwords must match')])
    confirm = PasswordField('Confirm', [Required(
                            "Password again, please.")])
    submit = SubmitField("submit")


class UnityForm(Form):
    """Class for new posts form."""

    title = TextField("Title", [Required(
                      "Please enter a title for your post.")])
    body = PageDownField("Body", [Required(
                         "Please enter a body to your post.")])
    summary = TextAreaField("Summary")
    tags = TagListField("Tags")
    source = TagListField("Source")
    postType = SelectField(
        "Post Type", choices=[
            ('draft', 'draft'),
            ('blog', 'blog post'),
            ('page', 'page')])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        """Retuns true if form valid, false if not."""
        if not Form.validate(self):
            return False
        else:
            return True

    def validate_with_slug(self):
        """
        Attempts to slugify `self.title.data` and find it in the db.  If found,
        returns an error saying it already exists.  If not found, it is unique
        and returns True.
        """
        if self.validate():
            try:
                newSlug = makeSlug(self.title.data)
                slug = Unity.objects.get(slug=newSlug)
                if slug:
                    self.title.errors.append("That title already exists.")
                    return False
            except DoesNotExist:
                return True

    def validate_on_update(self, slug):
        """
        On update/edit of a previously submitted post, checks to see whether
        the title/slug has changed.  If it has changed, it returns
        `self.validate_with_slug()`.  If it has not changed, it returns
        `self.validate()`.
        """
        if slug == makeSlug(self.title.data):
            return self.validate()
        else:
            return self.validate_with_slug()
