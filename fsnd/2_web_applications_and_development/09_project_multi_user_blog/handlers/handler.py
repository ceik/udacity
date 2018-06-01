import webapp2
import utils

from models.users import Users
from models.votes import Votes


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = utils.jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_cookie(self, user):
        cookie_val = utils.make_cookie_val(user.key().id())
        self.response.headers.add_header('Set-Cookie', 'name=%s;Path=/' %
                                         str(cookie_val))

    def get_user(self):
        cookie_val = self.request.cookies.get('name')
        if cookie_val:
            return Users.get_by_id(int(cookie_val.split('|')[0]))
        else:
            return None

    def vote(self, post, user, previous_vote, vote):
        post.votes += vote
        post.put()

        if previous_vote:
            previous_vote.vote += vote
            previous_vote.put()
        else:
            vote = Votes(post=post, user=user, vote=vote)
            vote.put()
