import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.api import users
from post import Post
from uploadhandler import UploadHandler
from google.appengine.api.images import get_serving_url
JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True
)

class AddPost(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()


        #If user is not found navigate to guest page and stop processing
        if user == None:
            template_values = {
            'login_url' : users.create_login_url(self.request.uri),
            }
            template = JINJA_ENVIRONMENT.get_template('mainguest.html')
            self.response.write(template.render(template_values))
            return


        #If user is found get the user and navigate to the main page
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        if myuser == None:
            myuser = MyUser(id=user.user_id())
            myuser.put()

        template_values = {
        'myuser':myuser,
        'upload_url' : blobstore.create_upload_url('/upload'),
        'get_serving_url': get_serving_url
        }
        template = JINJA_ENVIRONMENT.get_template('addpost.html')
        self.response.write(template.render(template_values))
