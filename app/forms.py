from flask.ext.wtf import Form, RecaptchaField
from wtforms import (TextField, TextAreaField, PasswordField,
                     SubmitField, BooleanField)
from wtforms.validators import Email, EqualTo, Required
from models import User, Post, Page
from mongoengine.queryset import DoesNotExist
from utils import makeSlug, CKTextAreaField


class LoginForm(Form):

    email = TextField('email', [Required(
                      "Please enter a username.")])
    password = PasswordField('password', [Required(
                             "Please enter a password")])
    remember_me = BooleanField('remember me')
    submit = SubmitField("login")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False

        try:
            user = User.objects.get(email=self.email.data.lower())
        except DoesNotExist:
            self.email.errors.append("Invalid email address")
            return False
        if user and user.check_password(self.password.data):
            return True
        else:
            self.password.errors.append("Invalid password")
            return False


class RegisterUser(Form):

    firstname = TextField("First name",  [Required(
                          "Please enter your first name.")])
    lastname = TextField("Last name",  [Required(
                         "Please enter your last name.")])
    email = TextField(
        "Email", [
            Required("Please enter your email address."),
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
        if not Form.validate(self):
            return False

        try:
            user = User.objects.get(email=self.email.data.lower())
            if user:
                self.email.errors.append("That email already exists.")
            return False
        except DoesNotExist:
            return True


class PostForm(Form):

    title = TextField("Title", [Required(
                      "Please enter a title for your post.")])
    body = CKTextAreaField("Body", [Required(
                           "Please enter a body to your post.")])
    tags = TextField("Tags")
    submit = SubmitField("Create Post")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        try:
            newSlug = makeSlug(self.title.data)
            slug = Post.objects.get(slug=newSlug)
            if slug:
                self.slug.errors.append("That title already exists.")
                return False
        except DoesNotExist:
            return True


class CommentForm(Form):

    comment = TextAreaField('comment', [Required()])
    submit = SubmitField("submit")


class PageForm(Form):

    title = TextField("Title", [Required(
                      "Please enter a title for your page.")])
    content = CKTextAreaField("Content", [Required(
                              "Please enter content for your page.")])
    submit = SubmitField("Submit Page")

    def validate(self):
        if not Form.validate(self):
            return False
        try:
            slug = makeSlug(self.title.data)
            page = Page.objects.get(slug=slug)
            if page:
                self.title.errors.append("That page already exists.")
                return False
        except DoesNotExist:
            return True
