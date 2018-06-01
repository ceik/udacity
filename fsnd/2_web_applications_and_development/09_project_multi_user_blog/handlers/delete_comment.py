from handler import Handler
from models.comments import Comments


class DeleteCommentHandler(Handler):
    def get(self, comment_id):
        comment = Comments.get_by_id(int(comment_id))
        user = self.get_user()
        if user and comment.created_by.key() == user.key():
            comment.delete()
            self.render("del_comment.html", comment=comment, success=True)
        else:
            self.render("del_comment.html", comment=comment, success=False)
