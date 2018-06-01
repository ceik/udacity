from handler import Handler
from utils import valid_email, valid_pw, valid_username
from utils import check_cookie_val, make_pw_hash
from models.users import Users

from google.appengine.ext import db


class SignupHandler(Handler):
    def get(self):
        cookie_val = self.request.cookies.get('name')
        if not cookie_val or not check_cookie_val(cookie_val):
            self.render("user_signup.html")
        else:
            self.redirect("/blog/welcome")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify_pw = self.request.get("verify")
        user_email = self.request.get("email")

        username_taken = db.GqlQuery("SELECT * FROM Users WHERE name = :1",
                                     username).get()

        if (valid_username(username) == '' or not valid_username(username)):
            self.render("user_signup.html",
                        username_error_message="That's not a valid username!",
                        user_email=user_email)
        elif not valid_pw(password):
            self.render("user_signup.html",
                        username=username,
                        upper_pw_error_message="That's not a valid password!",
                        user_email=user_email)
        elif password != verify_pw:
            self.render("user_signup.html",
                        username=username,
                        lower_pw_error_message="The passwords don't match!",
                        user_email=user_email)
        elif user_email != '' and not valid_email(user_email):
            self.render("user_signup.html",
                        username=username, user_email=user_email,
                        email_error_message="That's not a valid email!")
        elif username_taken:
            self.render("user_signup.html",
                        username_error_message="That name is already taken!",
                        user_email=user_email)
        else:
            pw_hash = make_pw_hash(username, password)
            user = Users(name=username, email=user_email, password=pw_hash)
            user.put()

            self.set_cookie(user)
            self.redirect("/blog/welcome")
