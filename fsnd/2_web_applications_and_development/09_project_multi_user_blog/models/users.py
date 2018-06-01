from google.appengine.ext import db


class Users(db.Model):
    name = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    created_at = db.DateTimeProperty(auto_now_add=True)
    email = db.StringProperty(required=False)
