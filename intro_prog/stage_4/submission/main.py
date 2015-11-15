# Submission Stage 4
# To run this: python "C:\Program Files (x86)\Google\google_appengine\dev_appserver.py" submission\

import os
import jinja2
import webapp2

# import guestbook.py
import cgi
import urllib
from google.appengine.api import users
from google.appengine.ext import ndb

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity. We use guestbook_name
    as the key."""
    return ndb.Key('Guestbook', guestbook_name)

class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)

class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)





template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
    autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    def get(self):
        self.render("main.html")

class Notes1Page(Handler):
    def get(self):
        self.render("notes_stage_1.html")

class Notes4Page(Handler):
    def get(self):
        self.render("notes_stage_4.html")





class GuestbookPage(Handler):
    def get(self):
        self.render("guestbook.html")





app = webapp2.WSGIApplication([
    ("/", MainPage),
    ("/notes1", Notes1Page),
    ("/notes4", Notes4Page),
    ("/guestbook", GuestbookPage)
])
