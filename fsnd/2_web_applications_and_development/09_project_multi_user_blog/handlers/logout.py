from handler import Handler


class LogoutHandler(Handler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'name='';Path=/')
        self.redirect("/blog/signup")
