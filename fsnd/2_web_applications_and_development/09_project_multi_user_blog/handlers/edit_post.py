from handler import Handler
from models.posts import Posts


class EditPostHandler(Handler):
    def get(self, post_id):
        post = Posts.get_by_id(int(post_id))
        user = self.get_user()

        if not user:
            self.redirect("/blog/login")
        else:
            self.render("edit_post.html", post=post, user=user)

    def post(self, post_id):
        post = Posts.get_by_id(int(post_id))
        subject = self.request.get("subject")
        content = self.request.get("content")
        user = self.get_user()

        if post.created_by.key() != user.key():
            self.redirect("/blog/login")

        elif subject and content:
            post.subject = subject
            post.content = content
            post.put()

            self.redirect("/blog/%s" % str(post.key().id()))

        else:
            error = "We need both a subject and some content!"
            self.render("edit_post.html", subject=subject, content=content,
                        error=error)
