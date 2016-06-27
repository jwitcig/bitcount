import json
import os

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.list import ListView, View
from django.views.generic.base import TemplateView, RedirectView

import requests
from requests_oauthlib import OAuth1

class LoginView(TemplateView):

    template_name = "twitter_login.html"

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['authenticate_url'] = reverse('login:authenticate')
        return context

class AuthenticateView(View):

    def get(self, request):
        oauth_token = ''
        oauth_token_secret = ''
        oauth_callback_confirmed = False

        auth = OAuth1(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'], os.environ['TWITTER_ACCESS_TOKEN_KEY'], os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

        token_url = 'https://api.twitter.com/' + 'oauth/request_token'
        response = requests.post(token_url, auth=auth, headers={'Content-Type': 'application/x-www-form-urlencoded'}, params={'oauth_callback': os.environ['SITE_URL'] + 'login/callback'})

        json_data = {}
        for data in response.text.split('&'):
            split_data = data.split('=')

            json_data[split_data[0]] = split_data[1]

        oauth_token = json_data['oauth_token']
        oauth_token_secret = json_data['oauth_token_secret']
        oauth_callback_confirmed = json_data['oauth_callback_confirmed']

        print('oauth_token: ' + oauth_token)
        print('oauth_token_secret: ' + oauth_token_secret)
        print('oauth_callback_confirmed: ' + oauth_callback_confirmed)

        return HttpResponseRedirect('https://api.twitter.com/oauth/authorize?oauth_token=' + oauth_token)

# class Login(TemplateView):
#
#     template_name = "home.html"
#
#     def get_context_data(self, **kwargs):
#         context = super(HomePageView, self).get_context_data(**kwargs)
#         context['latest_articles'] = Article.objects.all()[:5]
#         return context

class LoginCallback(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        oauth_data = self.request.GET.dict()

        oauth_token = oauth_data.get('oauth_token')
        oauth_verifier = oauth_data.get('oauth_verifier')

        if oauth_token == None or oauth_verifier == None:
            return 'fatal: redirect to failure to authenticate page'

        self.request.session['oauth_token'] = oauth_token
        self.request.session['oauth_verifier'] = oauth_verifier

        return reverse('login:success')

class LoginSuccessView(View):

    def get(self, request):
        auth = OAuth1(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'], os.environ['TWITTER_ACCESS_TOKEN_KEY'], os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

        auth = OAuth1(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'], request.session['oauth_token'], request.session['oauth_verifier'])
        access_token_url = settings.TWITTER_API_URL + 'oauth/access_token'
        response = requests.post('https://api.twitter.com/oauth/access_token', auth=auth, params={
                                                'oauth_verifier': request.session['oauth_verifier'],
                                                'oauth_token': request.session['oauth_token'],
                                            })

        json_data = {}
        for data in response.text.split('&'):
            split_data = data.split('=')

            json_data[split_data[0]] = split_data[1]

        request.session['oauth_token'] = json_data['oauth_token']
        request.session['oauth_token_secret'] = json_data['oauth_token_secret']
        request.session['oauth_verifier'] = None

        request.session['screen_name'] = json_data['screen_name']
        request.session['twitter_id'] = json_data['user_id']

        return HttpResponseRedirect(reverse('home:stats'))
