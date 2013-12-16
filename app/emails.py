"""
    app.emails
    ~~~~~~~~~

    All emailing funcitons needed throughout application.

    :copyright: and :license: see TOPMATTER.
"""

from flask.ext.mail import Message
from app import mail
from flask import render_template
from config import ADMINS
from decorators import async


@async
def send_async_email(msg):
    """
    Takes `msg` and emails it using `mail.send(msg)` as a background process.
    """
    mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    """
    Takes `subject`, `sender`, `recipients` (as a list), `text_body`,
    and `html_body`.  Creates message and calls `send_async_email(msg)`.
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(msg)


def email_confirmation(user, payload):
    """
    Takes `user` and `payload` and creates Email Confirmation email.
    """
    send_email(
        "[homelessgaffer.com] - confirm email",
        ADMINS[0],
        #[ADMINS[0]],
        [user.email],
        render_template("emails/email_confirmation.txt",
                        user=user,
                        payload=payload),
        render_template("emails/email_confirmation.html",
                        user=user,
                        payload=payload)
        )


def email_password_reset(user, payload):
    """
    Takes `user` and `payload` and creates Password Reset email.
    """
    send_email(
        "[homelessgaffer.com] - password reset",
        ADMINS[0],
        #[ADMINS[0]],
        [user.email],
        render_template("emails/password_reset.txt",
                        user=user,
                        payload=payload),
        render_template("emails/password_reset.html",
                        user=user,
                        payload=payload)
        )
