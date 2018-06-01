import webapp2

from handlers.mainpage import MainPageHandler
from handlers.new_post import NewPostHandler
from handlers.post import PostHandler
from handlers.edit_post import EditPostHandler
from handlers.new_comment import NewCommentHandler
from handlers.edit_comment import EditCommentHandler
from handlers.delete_comment import DeleteCommentHandler
from handlers.upvote import UpvoteHandler
from handlers.downvote import DownvoteHandler
from handlers.signup import SignupHandler
from handlers.login import LoginHandler
from handlers.logout import LogoutHandler
from handlers.welcome import WelcomeHandler

app = webapp2.WSGIApplication([
    ('/blog', MainPageHandler),
    ('/blog/', MainPageHandler),
    ('/blog/newpost', NewPostHandler),
    (r'/blog/(\d+)', PostHandler),
    (r'/blog/edit/(\d+)', EditPostHandler),
    (r'/blog/newcomment/(\d+)', NewCommentHandler),
    (r'/blog/editcomment/(\d+)', EditCommentHandler),
    (r'/blog/delcomment/(\d+)', DeleteCommentHandler),
    (r'/blog/upvote/(\d+)', UpvoteHandler),
    (r'/blog/downvote/(\d+)', DownvoteHandler),
    ('/blog/signup', SignupHandler),
    ('/blog/login', LoginHandler),
    ('/blog/logout', LogoutHandler),
    ('/blog/welcome', WelcomeHandler)], debug=True)
