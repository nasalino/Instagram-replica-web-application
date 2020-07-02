from google.appengine.ext import ndb
class Comments(ndb.Model):
    text = ndb.StringProperty()
    comment_time =ndb.StringProperty()
    comment_user = ndb.KeyProperty()
