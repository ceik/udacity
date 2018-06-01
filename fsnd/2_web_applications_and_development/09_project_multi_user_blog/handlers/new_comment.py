from handler import Handler
from models.posts import Posts
from models.comments import Comments


class NewCommentHandler(Handler):
    def get(self, post_id):
        user = self.get_user()
        if user:
            self.render("newcomment.html")
        else:
            self.redirect("/blog/login")

    def post(self, post_id):
        user = self.get_user()
        post = Posts.get_by_id(int(post_id))
        content = self.request.get("content")

        if content:
            new_comment = Comments(content=content, created_by=user, post=post)
            new_comment.put()

            self.redirect("/blog/%s" % str(post.key().id()))

        else:
            error = "We need some content!"
            self.render("newcomment.html", content=content, error=error)
