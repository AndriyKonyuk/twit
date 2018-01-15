from django.db import models
from django.contrib.auth.models import User



class Followers(models.Model):
    screen_name = models.CharField(max_length=100)
    id_foll = models.IntegerField()
    name_foll = models.CharField(max_length=100)
    user_img = models.CharField(max_length=100, default='None')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Tweets(models.Model):
    text = models.TextField()
    likes = models.IntegerField()
    retweet = models.IntegerField()
    date = models.DateTimeField()
    tweet_id = models.IntegerField()
    tweet_img_url = models.CharField(max_length=200, default='None')
    tweet_video_url = models.CharField(max_length=200, default='None')
    tweet_owner = models.ForeignKey(Followers, on_delete=models.CASCADE)


class Comments(models.Model):
    who_comment = models.CharField(max_length=100)
    text_comment = models.TextField()
    date = models.DateField()
    comment_owner = models.ForeignKey(Tweets, on_delete=models.CASCADE)





