import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api.images import get_serving_url

from datetime import datetime
from myuser import MyUser

JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True
)

class ProfilePage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()

        #If user is not found navigate to guest page and stop processing
        if user == None:
            template_values = {
            'login_url' : users.create_login_url(self.request.uri)
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

        key = self.request.GET['key']

        other_user_key = ndb.Key('MyUser', key)
        other_user = other_user_key.get()




        date_format = '%Y-%m-%d %H:%M:%S.%f'
        if other_user == myuser:
            posts = sorted(myuser.users_posts, key=lambda x: datetime.strptime(x.get().time, date_format),reverse=True)
        else:
            posts = sorted(other_user.users_posts, key=lambda x: datetime.strptime(x.get().time, date_format),reverse=True)

        template_values = {
        'logout_url' : users.create_logout_url(self.request.uri),
        'myuser' : myuser,
        'other_user':other_user,
        'other_user_key':other_user_key,
        'user':user,
        'get_serving_url': get_serving_url,
        'posts':posts
        }
        template = JINJA_ENVIRONMENT.get_template('profilepage.html')
        self.response.write(template.render(template_values))


    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        if self.request.get('button') == 'Follow':
            user = users.get_current_user()
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            key = self.request.GET['key']
            other_user_key = ndb.Key('MyUser', key)
            other_user = other_user_key.get()

            myuser.following_list.append(other_user_key)
            myuser.put()
            other_user.followers_list.append(myuser_key)
            other_user.put()
            self.redirect('/profilepage?key='+key)

        elif self.request.get('button') == 'Unfollow':
            user = users.get_current_user()
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            key = self.request.GET['key']
            other_user_key = ndb.Key('MyUser', key)
            other_user = other_user_key.get()

            index = -1
            for following in myuser.following_list:
                    index+=1
                    if following == other_user_key:
                        del myuser.following_list[index]
                        myuser.put()
            index = -1
            for followers in other_user.followers_list:
                    index+=1
                    if followers == myuser_key:
                        del other_user.followers_list[index]
                        other_user.put()

            self.redirect('/profilepage?key='+key)
