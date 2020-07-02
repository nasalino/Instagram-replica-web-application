from google.appengine.ext import ndb
from post import Post

#only place to use queries
class MyUser(ndb.Model):
    name = ndb.StringProperty()
    users_posts = ndb.KeyProperty(repeated=True)
    following_list = ndb.KeyProperty( repeated=True)
    followers_list = ndb.KeyProperty( repeated=True)
