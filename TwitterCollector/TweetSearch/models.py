from unittest.util import _MAX_LENGTH
from django.db import models

class Tweet(models.Model):
    t_id = models.CharField(max_length=100)
    t_text = models.TextField()
    t_hashtags = models.CharField(default='', max_length=250)
    t_username = models.CharField(max_length=100)
    t_nickname = models.CharField(max_length=100)
    t_likes = models.IntegerField()
    t_retweets = models.IntegerField()
    t_followers = models.IntegerField()
    t_verified = models.BooleanField()
    t_date = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return self.t_id +'-'+ self.t_username +'-'+ self.t_date.strftime('%d/%m/%Y at %H:%M')

