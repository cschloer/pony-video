from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    body = models.TextField()
    user = models.ForeignKey(User)

    def __unicode__(self):
        return "%s by user id %s, %s" % (self.title, self.user, self.created_date)



