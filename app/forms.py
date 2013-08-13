from flask.ext.wtf import Form, TextField, BooleanField, validators
from flask.ext.wtf import Required, PasswordField

class LoginForm(Form):
    username = TextField('username', [validators.Required()], default="doesn't work")
    password = PasswordField('password', [validators.Required()])

class RegisterUser(Form):
    username = TextField('username', [validators.Required()], default="doesn't work")
    password = PasswordField('password', [validators.Required(), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('password', [validators.Required()])
    email = TextField('email', [validators.Required()])
    acceptTOS = BooleanField('I accept the TOS', [validators.Required()])
    
