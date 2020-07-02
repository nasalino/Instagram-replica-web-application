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
from datetime import datetime
from google.appengine.api.images import get_serving_url
from followlist import FollowList
from comments import Comments
from datetime import datetime
from viewcomments import ViewComments


JINJA_ENVIRONMENT = jinja2.Environment(
loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
extensions=['jinja2.ext.autoescape'],
autoescape=True
)
#fix mobile diplay of home page
class MainPage(webapp2.RequestHandler):
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


        timeline = []
        for posts in myuser.users_posts:
            timeline.append(posts)
        for f in myuser.following_list:
            for posts in f.get().users_posts:
                timeline.append(posts)

        date_format = '%Y-%m-%d %H:%M:%S.%f'

#perform get here to get the post object from its key
        posts = sorted(timeline, key=lambda x: datetime.strptime(x.get().time, date_format),reverse=True)





        template_values = {
        'logout_url' : users.create_logout_url(self.request.uri),
        'myuser' : myuser,
        'upload_url' : blobstore.create_upload_url('/upload'),
        'get_serving_url': get_serving_url,
        #Only show the first 50 posts
        'posts':posts[:50]
        }
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        if action == 'post':
            comment = self.request.get('comment')
            key = self.request.GET['key']
            post_key =  ndb.Key('Post', int(key))
            post = post_key.get()
            now = datetime.now()


            user = users.get_current_user()
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()
            new_comment = Comments(text=comment, comment_time=str(now), comment_user=myuser_key)
            post.comments.append(new_comment)
            post.put()
            self.redirect('/')








app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/upload', UploadHandler),
    ('/addpost', AddPost),
    ('/edituser', EditUser),
    ('/profilepage' , ProfilePage),
    ('/viewcomments' , ViewComments),

    ('/search' ,Search),
    ('/followlist', FollowList)
    ], debug=True)
