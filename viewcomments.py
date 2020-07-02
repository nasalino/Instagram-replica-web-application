import os
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from myuser import MyUser
from post import Post
from uploadhandler import UploadHandler
from addpost import AddPost
from edituser import EditUser
from profilepage import ProfilePage
from search import Search
from comments import Comments
from datetime import datetime
from google.appengine.api.images import get_serving_url



JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True
)
#fix mobile diplay of home page
class ViewComments(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()


        #If user is not found navigate to guest page and stop processing
        if user == None:
            template_values = {
            'login_url' : users.create_login_url(self.request.uri),
            }
            template = JINJA_ENVIRONMENT.get_template('viewcommentst.html')
            self.response.write(template.render(template_values))
            return


        #If user is found get the user and navigate to the main page
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        if myuser == None:
            myuser = MyUser(id=user.user_id())
            myuser.put()

        key = self.request.GET['key']
        post_key =  ndb.Key('Post', int(key))
        post = post_key.get()



        template_values = {
        'logout_url' : users.create_logout_url(self.request.uri),
        'myuser' : myuser,
        'get_serving_url': get_serving_url,
        'i':post_key

        }
        template = JINJA_ENVIRONMENT.get_template('viewcomments.html')
        self.response.write(template.render(template_values))
