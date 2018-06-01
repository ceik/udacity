from handler import Handler


class WelcomeHandler(Handler):
    def get(self):
        user = self.get_user()
        if user:
            self.render("welcome.html", username=user.name)
        else:
            self.redirect("/blog/signup")
