from django.contrib import admin

from .models import TwitterData, DataRefresh

admin.site.register(TwitterData)
admin.site.register(DataRefresh)
