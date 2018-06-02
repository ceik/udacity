# "Database code" for the DB Forum.

import datetime
import psycopg2

POSTS = [("This is the first post.", datetime.datetime.now())]


def get_posts():
    """Return all posts from the 'database', most recent first."""
    pg = psycopg2.connect("dbname=forum")
    c = pg.cursor()
    c.execute("SELECT content, time FROM posts ORDER BY time DESC")
    rows = c.fetchall()
    pg.close()
    return rows


def add_post(content):
    """Add a post to the 'database' with the current timestamp."""
    pg = psycopg2.connect("dbname=forum")
    c = pg.cursor()
    c.execute("INSERT INTO posts VALUES (%s)", (content,))
    pg.commit()
    pg.close()
