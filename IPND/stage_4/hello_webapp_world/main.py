# Lession 4.5: Hello Webapp World
#
# This starter code will illustrate how we can create a webserver that writes out
# a "Hello World" to the browser usig the webapp2 library.

# https://www.udacity.com/course/viewer#!/c-nd000/l-4150259168/m-48722218

import webapp2

form="""
<form method="post" action="/testform">
    <input name="q">
    <input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        # self.response.headers["Content-Type"] = "text/plain"
        self.response.out.write(form)

class TestHandler(webapp2.RequestHandler):
    # def get(self):
    #     q = self.request.get("q")
    #     self.response.out.write(q)

    def post(self):
    #     q = self.request.get("q")
    #     self.response.out.write(q)


        # Using the code below, the browser will print the entire request!
        self.response.headers["Content-Type"] = "text/plain"
        self.response.out.write(self.request)

app = webapp2.WSGIApplication([("/", MainPage), ("/testform", TestHandler)],
    debug = True)
