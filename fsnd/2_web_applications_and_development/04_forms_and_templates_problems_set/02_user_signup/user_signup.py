import os
import jinja2
import webapp2
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PW_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


def valid_username(username):
    return USER_RE.match(username)


def valid_pw(password):
    return PW_RE.match(password)


def valid_email(email):
    return EMAIL_RE.match(email)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainPage(Handler):
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
        elif not email:
            self.render("user_signup.html",
                        user_username=user_username,
                        email_error_message="That's not a valid email!")
        else:
            self.redirect("/signup_success?username=" + user_username)


class SuccessHandler(Handler):
    def get(self):
        username = self.request.get("username")
        self.render("signup_success.html", username=username)


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/signup_success', SuccessHandler)],
                              debug=True)
