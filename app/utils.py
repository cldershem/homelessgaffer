"""
    app.utils
    ~~~~~~~~~

    Misc utility funcitons needed throughout application.

    :copyright: and :license: see TOPMATTER.
"""

from unicodedata import normalize
import re
from config import SECRET_KEY
from itsdangerous import (URLSafeSerializer, URLSafeTimedSerializer)
from jinja2 import Markup
from markdown import markdown
from app import app
from wtforms.fields import Field
from wtforms.widgets import TextInput


def makeSlug(text, delim=u'-'):
    """
    Takes a string and returns the url-safe, unicode equivelent.
    From http://flask.pocoo.org/snippets/5/ .
    """
    """Generates an slightly worse ASCII-only slug."""
    _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))


def get_serializer(secret_key=None):
    """Takes `secret_key` and returns url-safe, serialized equivielent."""
    if secret_key is None:
        secret_key = SECRET_KEY
    return URLSafeSerializer(secret_key)


def get_timed_serializer(secret_key=None):
    """
    Takes `secret_key` and returns url-safe, serialized equivielent which
    has a timestamp used to allow it to expire.
    """
    if secret_key is None:
        secret_key = SECRET_KEY
    return URLSafeTimedSerializer(secret_key)


@app.template_filter()
def markRight(markedText):
    """
    Takes a string, `markedText` and returns it after parsing for 'wikilink'
    and converting it to standard html.
    """
    return Markup(markdown(
        markedText,
        extensions=['wikilinks'],
        extension_configs={
            'wikilinks': [
                ('base_url', ''),
                ('end_url', ''),
                ('html_class', '')]}, safe_mode=False))


class TagListField(Field):
    """
    WTForms class widet to make a field to list post tags.
    """
    widget = TextInput()

    def _value(self):
        """Values on load."""
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, valuelist):
        """Converts string to list."""
        if valuelist:
            self.data = [x.strip() for x in valuelist[0].split(',')]
            self.data = filter(None, self.data)  # removes empty space
        else:
            self.data = []
