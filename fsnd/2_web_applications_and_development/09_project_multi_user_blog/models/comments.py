from google.appengine.ext import db

import posts
import users


class Comments(db.Model):
    content = db.TextProperty(required=True)
    post = db.ReferenceProperty(posts.Posts, required=True)
    created_at = db.DateTimeProperty(auto_now=True)
    created_by = db.ReferenceProperty(users.Users, required=True)
    updated_at = db.DateTimeProperty(auto_now=True)
