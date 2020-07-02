import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api.images import get_serving_url

from myuser import MyUser

JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True
)

class FollowList(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()

        key = self.request.GET['key']
        key_list = key.split('-')
        myuser_key = ndb.Key('MyUser', key_list[0])
        myuser = myuser_key.get()

        #If user is not found navigate to guest page and stop processing
        if user == None:
            template_values = {
            'login_url' : users.create_login_url(self.request.uri),
            }
            template = JINJA_ENVIRONMENT.get_template('mainguest.html')
            self.response.write(template.render(template_values))
            return





        template_values = {
        'logout_url' : users.create_logout_url(self.request.uri),
        'myuser' : myuser,

        'f':key_list[1]
        }
        template = JINJA_ENVIRONMENT.get_template('followlist.html')
        self.response.write(template.render(template_values))
