import os
import webapp2
import jinja2

import re
import string
import hashlib
import random

from google.appengine.ext import db

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


def make_salt():
    return ''.join(random.choice(string.letters) for x in range(5))


def make_hash(x, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(x + salt).hexdigest()
    return "%s|%s" % (h, salt)


def check_hash(x, h):
    salt = h.split('|')[1]
    return h == make_hash(x, salt)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Users(db.Model):
    name = db.StringProperty(required=True)
    password = db.TextProperty(required=True)
    name_hashed = db.TextProperty(required=True)
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)


class MainPageHandler(Handler):
    def get(self):
        self.write("Hello")


class SignupHandler(Handler):
    def get(self):
        self.render("user_signup.html")

    def post(self):
        user_username = self.request.get("username")
        user_password = self.request.get("password")
        user_verify = self.request.get("verify")
        user_email = self.request.get("email")

        username = valid_username(user_username)
        password = valid_pw(user_password)
        verify = valid_pw(user_verify)
        email = valid_email(user_email)

        if (username == '' or not username):
            self.render("user_signup.html",
                        username_error_message="That's not a valid username!",
                        user_email=user_email)
        elif not password:
            self.render("user_signup.html",
                        user_username=user_username,
                        upper_pw_error_message="That's not a valid password!",
                        user_email=user_email)
        elif user_password != user_verify:
            self.render("user_signup.html",
                        user_username=user_username,
                        lower_pw_error_message="The passwords don't match!",
                        user_email=user_email)
        elif user_email != '' and not email:
            self.render("user_signup.html",
                        user_username=user_username,
                        email_error_message="That's not a valid email!")
        else:
            name_hash = make_hash(user_username)
            pw_hash = make_hash(user_password)

            user = Users(name=user_username,
                         password=pw_hash,
                         name_hashed=name_hash)
            user.put()

            user_id = user.key().id()
            name_cookie_val = "%s|%s" % (user_id,
                                         name_hash.split('|')[0])
            self.response.headers.add_header('Set-Cookie', 'name=%s;Path=/' %
                                             str(name_cookie_val))

            self.redirect("/welcome")


class WelcomeHandler(Handler):
    def get(self):
        user_id = self.request.cookies.get('name').split('|')[0]
        username_hash = self.request.cookies.get('name').split('|')[1]
        user = Users.get_by_id(int(user_id))
        if username_hash != user.name_hashed.split('|')[0]:
            self.redirect("/signup")
        else:
            self.render("welcome.html", username=user.name)


class LoginHandler(Handler):
    def get(self):
        self.render("login.html")

    def post(self):
        user_username = self.request.get("username")
        user_password = self.request.get("password")

        username = valid_username(user_username)
        password = valid_pw(user_password)

        if (username == '' or not username):
            self.render("login.html",
                        username_error_message="That's not a valid username")
        elif not password:
            self.render("login.html",
                        user_username=user_username,
                        pw_error_message="That's not a valid password!")
        else:
            user_query = db.GqlQuery("SELECT * FROM Users where name = '%s'" %
                                     user_username).get()
            user_id = user_query.key().id()
            user_salt = user_query.name_hashed.split('|')[1]
            name_hash = make_hash(user_username, user_salt)
            name_cookie_val = "%s|%s" % (user_id,
                                         name_hash.split('|')[0])
            self.response.headers.add_header('Set-Cookie', 'name=%s;Path=/' %
                                             str(name_cookie_val))
            self.redirect("/welcome")


class LogoutHandler(Handler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'name='';Path=/')
        self.redirect("/signup")


app = webapp2.WSGIApplication([('/', MainPageHandler),
                               ('/signup', SignupHandler),
                               ('/welcome', WelcomeHandler),
                               ('/login', LoginHandler),
                               ('/logout', LogoutHandler)],
                              debug=True)
