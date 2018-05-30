# TODO: Fix pre tags (see videos on alternative)

import os
import webapp2
import jinja2

import re
import string
import hashlib
import hmac
import random

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PW_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

SECRET = 'sadf823*#nf*@nfoaisc*@N38fndsjfknu3q8n3#n3HS82'


def valid_username(username):
    return USER_RE.match(username)


def valid_pw(password):
    return PW_RE.match(password)


def valid_email(email):
    return EMAIL_RE.match(email)


def make_cookie_val(user_id):
    return '%s|%s' % (user_id, hmac.new(SECRET, str(user_id)).hexdigest())


def check_cookie_val(cookie_val):
    user_id = cookie_val.split('|')[0]
    if cookie_val == make_cookie_val(user_id):
        return user_id


def make_salt():
    return ''.join(random.choice(string.letters) for x in range(5))


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    pw_hash = hashlib.sha256(name + pw + salt).hexdigest()
    return "%s|%s" % (salt, pw_hash)


def check_pw_hash(name, pw, pw_hash):
    salt = pw_hash.split('|')[0]
    return pw_hash == make_pw_hash(name, pw, salt)


class Users(db.Model):
    name = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    created_at = db.DateTimeProperty(auto_now_add=True)
    email = db.StringProperty(required=False)


class Posts(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    votes = db.IntegerProperty(required=True, default=0)
    created_at = db.DateTimeProperty(auto_now_add=True)
    created_by = db.ReferenceProperty(Users)
    updated_at = db.DateTimeProperty(auto_now=True)


class Votes(db.Model):
    # Cause Like Buttons are creepy af
    post = db.ReferenceProperty(Posts, required=True)
    user = db.ReferenceProperty(Users, required=True)
    vote = db.IntegerProperty(required=True)
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)


class Comments(db.Model):
    content = db.TextProperty(required=True)
    post = db.ReferenceProperty(Posts, required=True)
    created_at = db.DateTimeProperty(auto_now=True)
    created_by = db.ReferenceProperty(Users, required=True)
    updated_at = db.DateTimeProperty(auto_now=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_cookie(self, user):
        cookie_val = make_cookie_val(user.key().id())
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


class MainPageHandler(Handler):
    def get(self):
        user = self.get_user()
        posts = db.GqlQuery(
            "SELECT * FROM Posts ORDER BY created_at DESC LIMIT 10")
        if user:
            self.render("front.html", posts=posts, logged_in=True)
        else:
            self.render("front.html", posts=posts, logged_in=False)


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

        if subject and content:
            new_post = Posts(subject=subject, content=content, created_by=user)
            new_post.put()

            self.redirect("/blog/%s" % str(new_post.key().id()))

        else:
            error = "We need both a subject and some content!"
            self.render("newpost.html", subject=subject, content=content,
                        error=error)


class PostHandler(Handler):
    def get(self, post_id):
        post = Posts.get_by_id(int(post_id))
        comments = db.GqlQuery("SELECT * FROM Comments WHERE post = :1 \
                               ORDER BY created_at ASC LIMIT 10",
                               post.key())
        self.render("post.html", post=post, comments=comments)


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

        if subject and content:
            post.subject = subject
            post.content = content
            post.put()

            self.redirect("/blog/%s" % str(post.key().id()))

        else:
            error = "We need both a subject and some content!"
            self.render("edit_post.html", subject=subject, content=content,
                        error=error)


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


class EdCommentHandler(Handler):
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

        if content:
            comment.content = content
            comment.put()

            self.redirect("/blog/%s" % str(comment.post.key().id()))

        else:
            error = "You can't leave an empty comment! If you want to delete \
                     the comment, use the link below."
            self.render("edit_comment.html", comment=comment,
                        content=content, error=error, user=user)


class DelCommentHandler(Handler):
    def get(self, comment_id):
        comment = Comments.get_by_id(int(comment_id))
        user = self.get_user()
        if user and comment.created_by.key() == user.key():
            comment.delete()
            self.render("del_comment.html", comment=comment, success=True)
        else:
            self.render("del_comment.html", comment=comment, success=False)


class UpvoteHandler(Handler):
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
                self.render("vote.html", post=post, user=user, upvote=True,
                            cheater=True, repeat_vote=False)
            elif previous_vote and previous_vote.vote == 1:
                self.render("vote.html", post=post, user=user, upvote=True,
                            cheater=False, repeat_vote=True)
            elif previous_vote and previous_vote.vote == -1:
                self.vote(post, user, previous_vote, vote=2)
                self.render("vote.html", post=post, user=user, upvote=True,
                            cheater=False, repeat_vote=False)
            else:
                self.vote(post, user, None, vote=1)
                self.render("vote.html", post=post, user=user, upvote=True,
                            cheater=False, repeat_vote=False)


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


class SignupHandler(Handler):
    def get(self):
        cookie_val = self.request.cookies.get('name')
        if not cookie_val or not check_cookie_val(cookie_val):
            self.render("user_signup.html")
        else:
            self.redirect("/blog/welcome")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify_pw = self.request.get("verify")
        user_email = self.request.get("email")

        username_taken = db.GqlQuery("SELECT * FROM Users WHERE name = :1",
                                     username).get()

        if (valid_username(username) == '' or not valid_username(username)):
            self.render("user_signup.html",
                        username_error_message="That's not a valid username!",
                        user_email=user_email)
        elif not valid_pw(password):
            self.render("user_signup.html",
                        username=username,
                        upper_pw_error_message="That's not a valid password!",
                        user_email=user_email)
        elif password != verify_pw:
            self.render("user_signup.html",
                        username=username,
                        lower_pw_error_message="The passwords don't match!",
                        user_email=user_email)
        elif user_email != '' and not valid_email(user_email):
            self.render("user_signup.html",
                        username=username, user_email=user_email,
                        email_error_message="That's not a valid email!")
        elif username_taken:
            self.render("user_signup.html",
                        username_error_message="That name is already taken!",
                        user_email=user_email)
        else:
            pw_hash = make_pw_hash(username, password)
            user = Users(name=username, email=user_email, password=pw_hash)
            user.put()

            self.set_cookie(user)
            self.redirect("/blog/welcome")


class LoginHandler(Handler):
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.request.get("username")
        pw = self.request.get("password")

        user = db.GqlQuery("SELECT * FROM Users where name = :1",
                           username).get()
        if not user or not check_pw_hash(username, pw, user.password):
            self.render("login.html",
                        username=username,
                        username_error_message="Invalid User/Password Combo!")
        else:
            self.set_cookie(user)
            self.redirect("/blog/welcome")


class LogoutHandler(Handler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'name='';Path=/')
        self.redirect("/blog/signup")

    def get(self):
        self.response.headers.add_header('Set-Cookie', 'name='';Path=/')
        self.redirect("/blog/signup")


class WelcomeHandler(Handler):
    def get(self):
        user = self.get_user()
        if user:
            self.render("welcome.html", username=user.name)
        else:
            self.redirect("/blog/signup")


app = webapp2.WSGIApplication([('/blog', MainPageHandler),
                               ('/blog/', MainPageHandler),
                               ('/blog/newpost', NewPostHandler),
                               (r'/blog/(\d+)', PostHandler),
                               (r'/blog/edit/(\d+)', EditPostHandler),
                               (r'/blog/newcomment/(\d+)', NewCommentHandler),
                               (r'/blog/editcomment/(\d+)', EdCommentHandler),
                               (r'/blog/delcomment/(\d+)', DelCommentHandler),
                               (r'/blog/upvote/(\d+)', UpvoteHandler),
                               (r'/blog/downvote/(\d+)', DownvoteHandler),
                               ('/blog/signup', SignupHandler),
                               ('/blog/login', LoginHandler),
                               ('/blog/logout', LogoutHandler),
                               ('/blog/welcome', WelcomeHandler)], debug=True)
