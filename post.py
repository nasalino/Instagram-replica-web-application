from google.appengine.ext import ndb
from comments import Comments
class Post(ndb.Model):
        user = ndb.KeyProperty()
        blob = ndb.BlobKeyProperty()
        caption  = ndb.StringProperty()
        time =ndb.StringProperty()
        hour =ndb.StringProperty()
        comments = ndb.StructuredProperty(Comments, repeated=True)
