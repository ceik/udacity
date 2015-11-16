# Submission Stage 4
# To run this: python "C:\Program Files (x86)\Google\google_appengine\dev_appserver.py" submission\

import os
import jinja2
import webapp2
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
    autoescape = True)

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

max_greetings = 10

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

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **kw):
        t = jinja_env.get_template(template)
        return t.render(kw)

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

class ErrorPage(Handler):
    def get(self):
        self.render("error.html")

class GuestbookPage(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **kw):
        t = jinja_env.get_template(template)
        return t.render(kw)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch(max_greetings)
        user = users.get_current_user()
        authors = []
        greeting_texts = []

        for greeting in greetings:
            if greeting.author:
                author = greeting.author.email
                if user and user.user_id() == greeting.author.identity:
                    authors.append(author + ' (You) wrote')
            else:
                authors.append('An anonymous person wrote:')
            greeting_texts.append(greeting.content)

        zipper = zip(authors, greeting_texts)

        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        sign_query_params = urllib.urlencode({'guestbook_name':
                                              guestbook_name})

        self.render("guestbook.html", zipper = zipper,
            sign_query_params = sign_query_params,
            guestbook_name = guestbook_name, url = url,
            url_linktext = url_linktext)

class Guestbook(webapp2.RequestHandler):
    def post(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = Author(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())

        greeting.content = self.request.get('content')

        if not greeting.content == '':
            greeting.put()

        if greeting.content == '':
            self.redirect('/error')
        else:
            query_params = {'guestbook_name': guestbook_name}
            self.redirect('/guestbook?' + urllib.urlencode(query_params))

app = webapp2.WSGIApplication([
    ("/", MainPage),
    ("/notes1", Notes1Page),
    ("/notes4", Notes4Page),
    ("/guestbook", GuestbookPage),
    ("/sign", Guestbook),
    ("/error", ErrorPage)
])
