from handler import Handler
from google.appengine.ext import db
from models.posts import Posts


class PostHandler(Handler):
    def get(self, post_id):
        post = Posts.get_by_id(int(post_id))
        comments = db.GqlQuery("SELECT * FROM Comments WHERE post = :1 \
                               ORDER BY created_at ASC LIMIT 10",
                               post.key())
        self.render("post.html", post=post, comments=comments)
