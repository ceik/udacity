# Submission Stage 5

import os
import jinja2
import webapp2
import urllib
import urllib2
from xml.dom import minidom
from google.appengine.api import users
from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
    autoescape = True)

DEFAULT_GUESTBOOK_NAME = 'submission_guestbook'

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
    coords = ndb.GeoPtProperty()

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **kw):
        t = jinja_env.get_template(template)
        return t.render(kw)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false"
IP_URL = "http://api.hostip.info/?ip="

def gmaps_img(points):
    img_url = GMAPS_URL
    for point in points:
         img_url += '&markers=' + str(point.lat) + ',' + str(point.lon)
    return img_url

def get_coords(ip):
	url = IP_URL + ip
	content = None
	try:
		content = urllib2.urlopen(url).read()
	except URLError:
		return

	if content:
		d = minidom.parseString(content)
		coords = d.getElementsByTagName("gml:coordinates")
		if coords and coords[0].childNodes[0].nodeValue:
			lon, lat = coords[0].childNodes[0].nodeValue.split(',')
			return ndb.GeoPt(lat, lon)

class MainPage(Handler):
    def get(self):
        self.render("main.html")

class Notes1Page(Handler):
    def get(self):
        self.render("notes_stage_1.html")

class Notes4Page(Handler):
    def get(self):
        self.render("notes_stage_4.html")

class Notes5Page(Handler):
    def get(self):
        self.render("notes_stage_5.html")

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

        points = filter(None, (a.coords for a in greetings))

        img_url = None
        if points:
            img_url = gmaps_img(points)

        self.render("guestbook.html", zipper = zipper,
            sign_query_params = sign_query_params,
            guestbook_name = guestbook_name, url = url,
            url_linktext = url_linktext, greetings = greetings,
            img_url = img_url)

class Guestbook(webapp2.RequestHandler):
    def post(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = Author(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())

        coords = get_coords(self.request.remote_addr)
        if coords:
            greeting.coords = coords

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
    ("/notes5", Notes5Page),
    ("/guestbook", GuestbookPage),
    ("/sign", Guestbook),
    ("/error", ErrorPage)
])
