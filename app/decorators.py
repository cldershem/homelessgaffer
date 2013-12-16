"""
    app.decorators
    ~~~~~~~~~

    All decorator functions needed throughout application.

    :copyright: and :license: see TOPMATTER.
"""

from threading import Thread
from functools import wraps
from flask import flash, redirect, url_for
from flask.ext.login import current_user


def async(func):
    """
    Enables process to run in background while page is loaded.
    """
    def wrapper(*args, **kwargs):
        thr = Thread(target=func, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def anon_required(func):
    """
    Antitheses of `LoginManager(app).login_required`, requires user to be
    logged out.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated():
            flash("Please logout to use this feature.")
            return redirect(url_for('index'))
        else:
            return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    """Admin privlidges required to access admin pages."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated():  # and current_user.roles.is_admin:
            return func(*args, **kwargs)
        else:
            flash("You must be an admin to access this page.")
            return redirect(url_for('index'))
    return wrapper
