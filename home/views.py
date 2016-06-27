from datetime import datetime, date
import json
import os

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.list import ListView, View

import requests
from requests_oauthlib import OAuth1

from home.models import TwitterData, DataRefresh

class DataListView(ListView):

    template_name = 'list.html'
    context_object_name = 'entries'

    def get_context_data(self, **kwargs):
        context = super(DataListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return self.get_data()

    def get_data(self):
        def get_or_create_data_entry(user_dict):
            twitter_data, created = TwitterData.objects.get_or_create(pk=user_dict['id'])
            twitter_data.screen_name = user_dict['screen_name']
            twitter_data.followers_count = user_dict['followers_count']
            twitter_data.friends_count = user_dict['friends_count']
            twitter_data.refreshed_date = datetime.now()
            twitter_data.save()
            return twitter_data

        next_cursor = -1
        entries = []

        current_user_id = self.request.session.get('twitter_id')

        if not current_user_id:
            return 'fatal: requires user_id'

        refresh, data_fetched_recently = DataRefresh.objects.get_or_create(user_id=current_user_id, date=date.today())

        if not data_fetched_recently:
            # fetch list of friends ids (allowed in higher quantity) and pull them from the DB
            ids = self.fetch_friends_ids(current_user_id, batch_size=500)
            return TwitterData.objects.filter(pk__in=ids)

        # fetch list of friends data (allowed in lesser quantity) and save them to the DB
        return [get_or_create_data_entry(user_dict) for user_dict in self.fetch_friends_data(current_user_id, batch_size=200)]

    def fetch_friends_ids(self, user_id, batch_size=500, cursor=-1):
        def fetch(self, user_id, batch_size, cursor):

            auth = OAuth1(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'], self.request.session['oauth_token'], self.request.session['oauth_token_secret'])
            url = settings.TWITTER_API_URL + 'friends/ids.json'

            params = {
                'count': batch_size,
                'user_id': user_id,
                'cursor': cursor,
            }

            response = requests.get(url, params=params, auth=auth)
            json_data = json.loads(response.text)
            return json_data['ids'], json_data['next_cursor']

        # remaining quantity : the max number of users to fetch
        remaining_batch_size = batch_size

        user_ids = []
        next_cursor = cursor
        while not next_cursor == 0 and remaining_batch_size > 0:
            ids, next_cursor = fetch(self, user_id, remaining_batch_size, next_cursor)
            remaining_batch_size = remaining_batch_size - len(ids)
            user_ids.extend(ids)
        return user_ids

    def fetch_friends_data(self, user_id, batch_size=200, cursor=-1):
        def fetch(self, user_id, batch_size, cursor):
            auth = OAuth1(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'], self.request.session['oauth_token'], self.request.session['oauth_token_secret'])
            url = settings.TWITTER_API_URL + 'friends/list.json'

            params = {
                'count': batch_size,
                'user_id': user_id,
                'cursor': cursor,
            }

            response = requests.get(url, params=params, auth=auth)
            json_data = json.loads(response.text)
            return json_data['users'], json_data['next_cursor']

        # remaining quantity : the max number of users to fetch
        remaining_batch_size = batch_size

        users = []
        next_cursor = cursor
        while not next_cursor == 0 and remaining_batch_size > 0:
            user_dicts, next_cursor = fetch(self, user_id, remaining_batch_size, next_cursor)
            remaining_batch_size = remaining_batch_size - len(user_dicts)
            users.extend(user_dicts)
        return users

def StatsView(ListView):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
