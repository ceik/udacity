import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Posts(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)


class MainPageHandler(Handler):
    def render_front(self):
        posts = db.GqlQuery("SELECT * FROM Posts ORDER BY created_at DESC")

        self.render("front.html", posts=posts)

    def get(self):
        self.render_front()


class NewPostHandler(Handler):
    def render_newpost(self, subject="", content="", error=""):
        self.render("newpost.html", subject=subject, content=content,
                    error=error)

    def get(self):
        self.render_newpost()

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            a = Posts(subject=subject, content=content)
            a.put()

            self.redirect("/%s" % str(a.key().id()))

        else:
            error = "We need both a subject and some content!"
            self.render_newpost(subject, content, error)


class PostHandler(Handler):
    def render_post(self, post_id):
        post = Posts.get_by_id(int(post_id))

        self.render("post.html", post=post)

    def get(self, post_id):
        self.render_post(post_id=post_id)


app = webapp2.WSGIApplication([(r'/', MainPageHandler),
                               (r'/newpost', NewPostHandler),
                               (r'/(\d+)', PostHandler)], debug=True)
