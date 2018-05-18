import os
import jinja2
import webapp2
import codecs

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


class MainPage(Handler):
    def get(self):
        self.render("rot_13.html")

    def post(self):
        input_text = self.request.get("text")
        rot_text = codecs.encode(input_text, 'rot_13')
        self.render("rot_13.html", old_text=rot_text)


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
