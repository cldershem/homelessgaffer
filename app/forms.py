from flask.ext.wtf import Form, RecaptchaField
from wtforms import (TextField, TextAreaField, PasswordField, SubmitField,
                     BooleanField)
from wtforms.validators import Email, EqualTo, Required
from models import User, Unity
from mongoengine.queryset import DoesNotExist
from utils import makeSlug, TagListField
from flask.ext.pagedown.fields import PageDownField


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
            user = User.objects.get(email=self.email.data.lower().strip())
            if user:
                self.email.errors.append("That email already exists.")
            return False
        except DoesNotExist:
            return True


class CommentForm(Form):

    comment = TextAreaField('comment', [Required()])
    submit = SubmitField("submit")


class ForgotPasswordForm(Form):

    email = TextField("email", [Required("Please enter your email.")])
    submit = SubmitField("submit")


class ResetPasswordForm(Form):

    password = PasswordField('New Password', [Required(),
                             EqualTo('confirm',
                                     message='Passwords must match')])
    confirm = PasswordField('Confirm', [Required(
                            "Password again, please.")])
    submit = SubmitField("submit")


class UnityForm(Form):

    title = TextField("Title", [Required(
                      "Please enter a title for your post.")])
    body = PageDownField("Body", [Required(
                         "Please enter a body to your post.")])
    summary = TextAreaField("Summary")
    tags = TagListField("Tags")
    source = TagListField("Source")
    isDraft = BooleanField("Save as draft?")
    isBlogPost = BooleanField("Publish to blog?")
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        else:
            return True

    def validate_with_slug(self):
        if self.validate():
            try:
                newSlug = makeSlug(self.title.data)
                slug = Unity.objects.get(slug=newSlug)
                if slug:
                    self.title.errors.append("That title already exists.")
                    return False
            except DoesNotExist:
                return True
