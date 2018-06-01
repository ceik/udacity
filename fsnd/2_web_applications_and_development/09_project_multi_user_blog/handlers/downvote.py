from handler import Handler
from models.posts import Posts
from google.appengine.ext import db


class DownvoteHandler(Handler):
    def get(self, post_id):
        post = Posts.get_by_id(int(post_id))
        user = self.get_user()

        if not user:
            self.redirect("/blog/login")
        else:
            previous_vote = db.GqlQuery("SELECT * FROM Votes WHERE post = :1 \
                                        AND user = :2",
                                        post.key(), user.key()).get()
            if user.key() == post.created_by.key():
                self.render("vote.html", post=post, user=user, upvote=False,
                            cheater=True, repeat_vote=False)
            elif previous_vote and previous_vote.vote == -1:
                self.render("vote.html", post=post, user=user, upvote=False,
                            cheater=False, repeat_vote=True)
            elif previous_vote and previous_vote.vote == 1:
                self.vote(post, user, previous_vote, vote=-2)
                self.render("vote.html", post=post, user=user, upvote=False,
                            cheater=False, repeat_vote=False)
            else:
                self.vote(post, user, None, vote=-1)
                self.render("vote.html", post=post, user=user, upvote=False,
                            cheater=False, repeat_vote=False)
