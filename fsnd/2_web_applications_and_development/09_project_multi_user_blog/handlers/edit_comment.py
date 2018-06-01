from handler import Handler
from models.comments import Comments


class EditCommentHandler(Handler):
    def get(self, comment_id):
        comment = Comments.get_by_id(int(comment_id))
        user = self.get_user()
        if user:
            self.render("edit_comment.html", comment=comment,
                        content=comment.content, user=user)
        else:
            self.redirect("/blog/login")

    def post(self, comment_id):
        comment = Comments.get_by_id(int(comment_id))
        user = self.get_user()
        content = self.request.get("content")

        if comment.created_by.key() != user.key():
            self.redirect("/blog/login")

        elif content:
            comment.content = content
            comment.put()

            self.redirect("/blog/%s" % str(comment.post.key().id()))

        else:
            error = "You can't leave an empty comment! If you want to delete \
                     the comment, use the link below."
            self.render("edit_comment.html", comment=comment,
                        content=content, error=error, user=user)
