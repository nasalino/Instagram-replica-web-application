from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
from post import Post
from myuser import MyUser
from google.appengine.api import users
from datetime import datetime
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload = self.get_uploads()[0]
        blobinfo = blobstore.BlobInfo(upload.key())


        new_post = Post()
        new_post.blob = upload.key()
        caption = self.request.get('caption')
        new_post.caption= caption

        now = datetime.now()
        new_post.time  = str(now)
        new_post.hour = str(now.hour)+':' + str(now.minute)+'    '+ str(now.day)+'-' + str(now.month)+'-' + str(now.year)

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        new_post.user = myuser_key

        post_key = new_post.put()


        #post_id = post_key.id()

        myuser.users_posts.append(post_key)
        myuser.put()
        self.redirect('/')
