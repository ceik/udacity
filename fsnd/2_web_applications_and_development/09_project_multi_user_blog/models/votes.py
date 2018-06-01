from google.appengine.ext import db

import posts
import users


class Votes(db.Model):
    # Cause Like Buttons are creepy af
    post = db.ReferenceProperty(posts.Posts, required=True)
    user = db.ReferenceProperty(users.Users, required=True)
    vote = db.IntegerProperty(required=True)
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)
