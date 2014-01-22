#!/usr/bin/env python

"""
    manage.py

    Functions to do some basic, bare metal setup/maintenence.
"""

import os
import sys
from flask.ext.script import (Manager, Server, prompt_pass, prompt)
from app import app
# from app.emails import email_confirmation


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    # use_debugger=True,
    # use_reloader=True,
    # host='0.0.0.0'
    )
)


@manager.command
def run():
    """Runs development server.  Replaces run.py"""
    app.config.update(dict(
        DEBUG=True,
        TESTING=True,
        testing=True,
        Testing=True,
        ))
    app.testing = True
    app.run()


@manager.command
def create_admin():
    """Creates a default administrator."""
    from app.forms import RegisterUser
    from werkzeug.datastructures import MultiDict
    from app.models import User

    app.testing = True
    firstname = prompt("What be your first name?").title()
    lastname = prompt("What is your last name?").title()
    email = prompt("What be your email?").lower().strip()
    password = prompt_pass("Please enter a password")
    confirm = prompt_pass("Please confirm password")
    recaptcha = ''
    data = MultiDict(dict(
        firstname=firstname,
        lastname=lastname,
        email=email,
        password=password,
        confirm=confirm,
        recaptcha=recaptcha
        ))

    form = RegisterUser(data, csrf_enabled=False)

    if not form.validate():
        print form.errors
        return create_admin()
    else:
        newUser = User(firstname=form.firstname.data.title(),
                       lastname=form.lastname.data.title(),
                       email=form.email.data.lower().strip())
        newUser.set_password(form.password.data)
        # payload = User.get_activation_link(newUser)
        # email_confirmation(newUser, payload)
        # print("Please confirm your email address by checking your email.")
        newUser.roles.is_admin = True
        newUser.roles.can_login = True
        newUser.save()
        try:
            user = User.get(email=form.email.data.lower().strip())
            if user.is_admin() is True and user.roles.can_login is True:
                pass
        except:
            print('There was an error adding your username to the db.')
        print("{} has been added as an admin.".format(user.email))


@manager.command
def migrate_db():
    """Migrate db from version to version."""
    pass


@manager.command
def backup_db():
    """Backups db locally and remotely."""
    pass


@manager.command
def restore_db():
    """Restores db from backup."""
    pass


@manager.command
def populate_db():
    """Populates db with dummy data for testing purposes."""
    pass


@manager.command
def show_config():
    """Prints config variables"""
    from pprint import pprint
    print("Config:")
    pprint(dict(app.config))


if __name__ == "__main__":
    manager.run()
