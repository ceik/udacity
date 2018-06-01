from google.appengine.ext import db
from handler import Handler


class MainPageHandler(Handler):
    def get(self):
        user = self.get_user()
        posts = db.GqlQuery(
            "SELECT * FROM Posts ORDER BY created_at DESC LIMIT 10")
        if user:
            self.render("front.html", posts=posts, logged_in=True)
        else:
            self.render("front.html", posts=posts, logged_in=False)
