#!/usr/bin/env python

"""
    manage.py

    Functions to do some basic, bare metal setup/maintenence.
"""

import os
import sys
from flask.ext.script import (Manager, Server, prompt_pass, prompt)
from app import app


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
        testing=True
        ))
    app.run()


@manager.command
def create_admin():
    """Creates a default administrator."""
    from app.forms import RegisterUser
    from werkzeug.datastructures import MultiDict
    # from app.models import User

    firstname = prompt("What be your first name?").title()
    lastname = prompt("What is your last name?").title()
    email = prompt("What be your email?").lower().strip()
    password = prompt_pass("Please enter a password")
    confirm = prompt_pass("Please confirm password")
    # recaptcha = True
    data = MultiDict(dict(
        firstname=firstname,
        lastname=lastname,
        email=email,
        password=password,
        confirm=confirm,
        # recaptcha=recaptcha
        ))

    form = RegisterUser(data, csrf_enabled=False)

    if not form.validate():
        print form.errors
        return create_admin()
    else:
        print(firstname, lastname, email, password, confirm)
        print("success")
        # newUser = User(firstname=form.firstname.data.title(),
        #                lastname=form.lastname.data.title(),
        #                email=form.email.data.lower().strip())
        # newUser.set_password(form.password.data)
        # newUser.save()
        # payload = get_activation_link(newUser)
        # email_confirmation(newUser, payload)
        # print("Please confirm your email address.")
        # return redirect(url_for('index'))


@manager.command
def migrate_db():
    """Migrate db from version to version."""
    pass


@manager.command
def backup_db():
    """Backups db locally and remotely."""
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
