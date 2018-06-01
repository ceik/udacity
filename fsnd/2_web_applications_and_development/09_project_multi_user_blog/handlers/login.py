from handler import Handler
from google.appengine.ext import db
from utils import check_pw_hash


class LoginHandler(Handler):
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.request.get("username")
        pw = self.request.get("password")

        user = db.GqlQuery("SELECT * FROM Users where name = :1",
                           username).get()
        if not user or not check_pw_hash(username, pw, user.password):
            self.render("login.html",
                        username=username,
                        username_error_message="Invalid User/Password Combo!")
        else:
            self.set_cookie(user)
            self.redirect("/blog/welcome")
