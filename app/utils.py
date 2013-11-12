from unicodedata import normalize
import re
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from config import SECRET_KEY
from itsdangerous import (URLSafeSerializer, BadSignature,
                          URLSafeTimedSerializer, SignatureExpired)
from jinja2 import Markup
from markdown import markdown
from app import app


def makeSlug(text, delim=u'-'):
    """Generates an slightly worse ASCII-only slug."""
    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


def get_serializer(secret_key=None):
    if secret_key is None:
        secret_key = SECRET_KEY
    return URLSafeSerializer(secret_key)


def get_activation_link(user):
    user_id = user.get_id()
    s = get_serializer()
    payload = s.dumps(user_id)
    return payload


def check_activation_link(payload):
    s = get_serializer()
    try:
        user_id = s.loads(payload)
    except BadSignature:
        return False
    return user_id


def get_timed_serializer(secret_key=None):
    if secret_key is None:
        secret_key = SECRET_KEY
    return URLSafeTimedSerializer(secret_key)


def get_password_reset_link(user):
    user_id = user.get_id()
    s = get_timed_serializer()
    payload = s.dumps(user_id)
    return payload


def check_password_reset_link(payload):
    s = get_timed_serializer()
    try:
        user_id = s.loads(payload, max_age=86400)
    except SignatureExpired or BadSignature:
        return False
    return user_id


@app.template_filter()
def markRight(markedText):
    return Markup(
        markdown(
            markedText,
            extensions=['wikilinks'],
            extension_configs={
                'wikilinks': [
                    ('base_url', ''),
                    ('end_url', ''),
                    ('html_class', '')]}, safe_mode=False))
