from datetime import datetime, timedelta, date

from django.db import models

class TwitterData(models.Model):

    followers_count = models.PositiveIntegerField(default=0)
    friends_count = models.PositiveIntegerField(default=0)

    user_id = models.TextField(primary_key=True)
    screen_name = models.TextField(default='')

    refreshed_date = models.DateField(default=date.today())

    @property
    def ratio(self):
        if self.friends_count == 0:
            return 0
        return self.followers_count / self.friends_count

    @property
    def needs_refresh(self):
        return datetime.now() - self.refreshed_date >= timedelta(days=1)

    def __str__(self):
        return self.user_id

class DataRefresh(models.Model):

    user_id = models.TextField(primary_key=True)
    date = models.DateTimeField(default=date.today())
