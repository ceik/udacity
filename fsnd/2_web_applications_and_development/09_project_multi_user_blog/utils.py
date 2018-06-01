import os
import jinja2

import hashlib
import hmac
import random
import re
import string

from config import SECRET


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PW_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")


def valid_username(username):
    return USER_RE.match(username)


def valid_pw(password):
    return PW_RE.match(password)


def valid_email(email):
    return EMAIL_RE.match(email)


def make_cookie_val(user_id):
    return '%s|%s' % (user_id, hmac.new(SECRET, str(user_id)).hexdigest())


def check_cookie_val(cookie_val):
    user_id = cookie_val.split('|')[0]
    if cookie_val == make_cookie_val(user_id):
        return user_id


def make_salt():
    return ''.join(random.choice(string.letters) for x in range(5))


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    pw_hash = hashlib.sha256(name + pw + salt).hexdigest()
    return "%s|%s" % (salt, pw_hash)


def check_pw_hash(name, pw, pw_hash):
    salt = pw_hash.split('|')[0]
    return pw_hash == make_pw_hash(name, pw, salt)
