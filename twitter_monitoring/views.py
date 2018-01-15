from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.db import Error
from oauthlib.uri_validate import query

from twitter_monitoring.forms import LoginForm, RegForm, Search
from django.contrib.auth.models import User
from twitter_monitoring.models import Followers, Tweets, Comments
import tweepy
import json


def twet_api():
    consumer_key = '3AwqU3oFqX7bVqLMD3llSnw6A'
    consumer_secret = 'OsbgqKRMxgxArjc19naWZjT1CppvxblvV7fJxf7fdxV7QrBHVc'
    access_token = '951536660596051968-JeLCf15Gq61eOu76vlVfeBB8hPLW8P6'
    access_token_secret = 'nuE2Jco5ZpXEgowfFtYbsK9trz2UZNHs9JbhNITAjHs82'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    return api


def vlogin(request):
    myd = {}
    myd['form'] = LoginForm()

    if request.POST:
        u_name = request.POST['user_name']
        u_pass = request.POST['user_pass']

        user = authenticate(request, username=u_name, password=u_pass)
        if user is not None:
            login(request, user)
            return redirect('/main')
        else:
            myd['form'] = LoginForm(request.POST)
    return render(request, 'twit/login.html', myd)


def vregister(request):
    form = RegForm()

    if request.POST:
        r = request.POST
        u_name = r['user_name']
        u_pass = r['user_pass']
        u_email = r['user_email']
        user = User.objects.create_user(u_name, u_email, u_pass)
        user.save()

    myd = {
        'form': form
    }
    return render(request, 'twit/reg.html', myd)


def vlogout(request):
    logout(request)
    return redirect('/singin')


@login_required
def vmain(request):
    myd = {}
    # foll_list = Followers.objects.filter(user_id=request.user)
    query_tweet = []
    test = Followers.objects.filter(user_id=request.user).prefetch_related('tweets_set')
    temp = []
    for i in test:
        temp.append(Tweets.objects.filter(tweet_owner=i))

    q = 0
    for i in temp:
        if q:
            q = q|i
        else:
            q = i

    q_s = q.distinct().order_by('-date')
    print(q_s)
    # q = Tweets.objects.all().filter(tweet_owner=foll)
    # myd['q_s'] = q_s
    myd['query_tweet'] = q_s
    myd['req'] = request
    # myd['test'] = test

    return render(request, 'twit/main.html', myd)


@login_required
def vsearch(request):
    myd = {}
    api = twet_api()

    if request.POST:
        r = request.POST
        search_user = api.get_user(r['search_input'])._json
        if search_user:
            myd['mess'] = {'good': 'User found!'}
        else:
            myd['mess'] = {'error': 'User not found!'}

        if 'action' in r and r['action'] == 'add':
            user_img = search_user['profile_image_url'].replace('normal', '400x400')
            obj, create = Followers.objects.get_or_create(screen_name=search_user['screen_name'],
                                                          id_foll=search_user['id_str'],
                                                          name_foll=search_user['name'], user_id=request.user,
                                                          user_img=user_img)
            if create:
                obj.save()
            else:
                myd.pop('good', None)
                myd['mess'] = {'info': 'User is in your list!'}


        elif 'action' in r and r['action'] == 'del':
            f = Followers.objects.get(screen_name=r['search_input'].replace('@', ''), user_id=request.user)
            f.delete()

    follow_list = Followers.objects.all().filter(user_id=request.user)
    if follow_list:
        myd['follow_list'] = follow_list
    else:
        myd['follow_list'] = []
    myd['form'] = Search()
    myd['req'] = request
    return render(request, 'twit/search.html', myd)


@login_required
def single_tweet(request, tweet_id):
    myd = {}
    foll_list = Followers.objects.filter(user_id=request.user)
    for foll in foll_list:
        q = Tweets.objects.all().filter(tweet_owner=foll).filter(tweet_id=tweet_id)
        f_info = foll.name_foll, foll.screen_name, foll.user_img
        myd['f_info'] = f_info
        if q.exists():
            myd['single_tweet'] = q[0]
            myd['req'] = request
            return render(request, 'twit/single.html', myd)
        else:
            if len(foll_list) > list(foll_list).index(foll):
                continue
            else:
                raise Http404('Tweet with this id: %s doesn\'t exist!' % tweet_id)
