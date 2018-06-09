#!/usr/bin/python2

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant
import re

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


class WebserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "Hello!"
                output += """
                    <form method='POST' enctype='multipart/form-data'
                    action='/hello'><h2>What would you like me to say?</h2>
                    <input name='message' type='text'>
                    <input type='submit' value='Submit'></form>
                    """
                output += "</html></body>"
                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                restaurants = session.query(Restaurant).all()

                output = ""
                output += "<html><body>"
                for r in restaurants:
                    output += "<br><div>%s</div>" % r.name
                    output += """
                        <a href="http://localhost:8080/restaurant/%s/edit">
                        Edit</a>
                        """ % r.id
                    output += """
                        <a href="http://localhost:8080/restaurant/%s/delete">
                        Delete</a>
                        """ % r.id
                    output += "<br><hr>"
                output += "</html></body>"
                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h2>Make a New Restaurant</h2>"
                output += """
                    <form method='POST' enctype='multipart/form-data'
                    action='/restaurants/new'>
                    <input name='new_name' type='text'>
                    <input type='submit' value='Create'></form>
                    """
                output += "</html></body>"
                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                path_id = re.search('\d+', self.path).group(0)
                print(path_id)

                r = session.query(Restaurant).filter_by(id=path_id).one()

                output = ""
                output += "<html><body>"
                output += "<h2>%s</h2>" % r.name
                output += """
                    <form method='POST' enctype='multipart/form-data'
                    action='/restaurants/%s/edit'>
                    <input name='edited_name' type='text'>
                    <input type='submit' value='Submit'></form>
                    """ % r.id
                output += "</html></body>"
                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                path_id = re.search('\d+', self.path).group(0)
                print(path_id)

                r = session.query(Restaurant).filter_by(id=path_id).one()

                output = ""
                output += "<html><body>"
                output += "<h2>Sure you want to delete %s?</h2>" % r.name
                output += """
                    <form method='POST' enctype='multipart/form-data'
                    action='/restaurants/%s/delete'>
                    <input type='submit' value='Delete'></form>
                    """ % r.id
                output += "</html></body>"
                self.wfile.write(output)
                print(output)
                return

        except IOError:
            self.send_error(404, "File not found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(301)
                self.end_headers()

                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')

                output = ""
                output += "<html><body>"
                output += "<h2>Okay, how about this</h2>"
                output += "<h1>%s</h1>" % messagecontent[0]
                output += """
                    <form method='POST' enctype='multipart/form-data'
                    action='/hello'><h2>What would you like me to say?</h2>
                    <input name='message' type='text'>
                    <input type='submit' value='Submit'></form>
                    """
                output += "</html></body>"
                self.wfile.write(output)
                print(output)

            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_name = fields.get('new_name')[0]

                print(new_name)
                new_restaurant = Restaurant(name=new_name)
                session.add(new_restaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                return

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    edited_name = fields.get('edited_name')[0]

                print(edited_name)
                path_id = re.search('\d+', self.path).group(0)
                print(path_id)

                r = session.query(Restaurant).filter_by(id=path_id).one()
                if r != []:
                    r.name = edited_name
                    session.add(r)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-Type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

                return

            if self.path.endswith("/delete"):
                path_id = re.search('\d+', self.path).group(0)
                print(path_id)

                r = session.query(Restaurant).filter_by(id=path_id).one()
                if r != []:
                    session.delete(r)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-Type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

                return

        except IOError:
            self.send_error(404, "File not found %s" % self.path)


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebserverHandler)
        print("Webserver running on port %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping webserver...")
        server.socket.close()


if __name__ == '__main__':
    main()
