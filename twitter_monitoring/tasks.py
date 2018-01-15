from __future__ import absolute_import, unicode_literals
from twitter_monitoring.models import Tweets, Comments, Followers
from celery import shared_task
from twitter_monitoring.views import twet_api
import tweepy
from celery.schedules import crontab
from celery.task import periodic_task
from django.db import Error
from datetime import timedelta
from django.contrib.auth.models import User
import time
import json


# object►extended_entities►media►0►video_info►variants►0►url
# object►extended_entities►media►0►media_url

@periodic_task(run_every=timedelta(minutes=1)) #hours=6 minutes=1
def update_tweets():
    user_list = User.objects.all()
    api = twet_api()

    for user in user_list:
        follower_list = Followers.objects.all().filter(user_id=user.id)

        for foll in follower_list:
            all_tweets = tweepy.Cursor(api.user_timeline, screen_name=foll.screen_name).items(20)
            for tw in all_tweets:
                i = tw._json
                i_j = json.dumps(i)
                i_date = time.strftime('%Y-%m-%d %H:%M:%S',
                                       time.strptime(i['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))

                if 'extended_entities' in i.keys():
                    if 'video_info' in i_j:
                        video = i['extended_entities']['media'][0]['video_info']['variants'][0]['url']
                        obj, create = Tweets.objects.get_or_create(text=i['text'], likes=i['favorite_count'],
                                                                   retweet=i['retweet_count'], date=i_date,
                                                                   tweet_owner=foll, tweet_id=i['id'],
                                                                   tweet_video_url=video)
                        obj.save()

                    elif 'media_url' in i_j:
                        img = i['extended_entities']['media'][0]['media_url']
                        obj, create = Tweets.objects.get_or_create(text=i['text'], likes=i['favorite_count'],
                                                                   retweet=i['retweet_count'], date=i_date,
                                                                   tweet_owner=foll, tweet_id=i['id'], tweet_img_url=img)
                        obj.save()
                else:
                    obj, create = Tweets.objects.get_or_create(text=i['text'], likes=i['favorite_count'],
                                                                   retweet=i['retweet_count'], date=i_date,
                                                                   tweet_owner=foll, tweet_id=i['id'])
                    obj.save()
