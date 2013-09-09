from threading import Thread
from functools import wraps
from flask import flash, redirect, url_for
from flask.ext.login import current_user


def async(func):
    """
    enables process to run in background while page is loaded
    """
    def wrapper(*args, **kwargs):
        thr = Thread(target=func, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def anon_required(func):
    """antitheses of login_required"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated():
            flash("Please logout to use this feature.")
            return redirect(url_for('index'))
        else:
            return func(*args, **kwargs)
    return wrapper
