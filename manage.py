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
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0'
    )
)


@manager.command
def run():
    """Runs development server.  Replaces run.py"""
    app.run()


@manager.command
def create_admin():
    """Creates a default administrator."""
    name = prompt("What be your full name?")
    email = prompt("What be your email?")
    pwd = prompt_pass("Please enter a password")
    pwd_confirm = prompt_pass("Please confirm password")
    print(name, email, pwd, pwd_confirm)


@manager.command
def migrate_db():
    """Runs script to migrate db from version to version."""
    pass


@manager.command
def backup_db():
    """Backups db locally and remotely."""
    pass


@manager.command
def populate_db():
    """Populates db with dummy data for testing purposes."""
    pass

if __name__ == "__main__":
    manager.run()
