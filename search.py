import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.api import users
from post import Post
from uploadhandler import UploadHandler
from myuser import MyUser
JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True
)
#what to do if only one range is inputed
#make checks non case sensitive

class Search(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'


        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        if myuser == None:
            myuser = MyUser(id=user.user_id())
            myuser.put()
        search_list=''
        template_values = {
        'myuser':myuser,
        'search_list': search_list
        }
        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))






    def post(self):
        action = self.request.get('button')

        if action == 'Search':
            #Retrieve user input
            name = self.request.get('name')




#If nothing is selceted display all ev's in the db
            if not name :

                user = users.get_current_user()
                myuser_key = ndb.Key('MyUser', user.user_id())
                myuser = myuser_key.get()
                query = MyUser.query()
                template_values = {
                'myuser':myuser,
                'search_list': query
                }
                template = JINJA_ENVIRONMENT.get_template('search.html')
                self.response.write(template.render(template_values))


            else:

                query = MyUser.query()
                search_list = []
                for i in query:
                    if name.lower() in i.name.lower():
                        search_list.append(i)


                user = users.get_current_user()
                myuser_key = ndb.Key('MyUser', user.user_id())
                myuser = myuser_key.get()

                template_values = {
                'myuser':myuser,
                'search_list': search_list
                }
                template = JINJA_ENVIRONMENT.get_template('search.html')
                self.response.write(template.render(template_values))








            #self.redirect('/searchEV')
