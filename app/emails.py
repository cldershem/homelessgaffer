from flask.ext.mail import Message
from app import mail
from flask import render_template
from config import ADMINS
from decorators import async


@async
def send_async_email(msg):
    mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(msg)


def email_confirmation(user, payload):
    send_email(
        "[homelessgaffer.com] - confirm email",
        ADMINS[0],
        [ADMINS[0]],  # change this to user.email?
        render_template("emails/email_confirmation.txt",
                        user=user,
                        payload=payload),
        render_template("emails/email_confirmation.html",
                        user=user,
                        payload=payload)
        )


def email_password_reset(user, payload):
    send_email(
        "[homelessgaffer.com] - confirm email",
        ADMINS[0],
        [ADMINS[0]],  # change this to user.email?
        render_template("emails/password_reset.txt",
                        user=user,
                        payload=payload),
        render_template("emails/password_reset.html",
                        user=user,
                        payload=payload)
        )