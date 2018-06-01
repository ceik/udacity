from handler import Handler
from models.posts import Posts


class NewPostHandler(Handler):
    def get(self):
        user = self.get_user()
        if user:
            self.render("newpost.html")
        else:
            self.redirect("/blog/login")

    def post(self):
        user = self.get_user()
        subject = self.request.get("subject")
        content = self.request.get("content")

        if not user:
            self.redirect("/blog/login")

        elif subject and content:
            new_post = Posts(subject=subject, content=content,
                             created_by=user)
            new_post.put()

            self.redirect("/blog/%s" % str(new_post.key().id()))

        else:
            error = "We need both a subject and some content!"
            self.render("newpost.html", subject=subject, content=content,
                        error=error)
