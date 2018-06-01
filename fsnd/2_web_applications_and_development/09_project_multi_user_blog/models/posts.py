from google.appengine.ext import db

import users


class Posts(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    votes = db.IntegerProperty(required=True, default=0)
    created_at = db.DateTimeProperty(auto_now_add=True)
    created_by = db.ReferenceProperty(users.Users)
    updated_at = db.DateTimeProperty(auto_now=True)
