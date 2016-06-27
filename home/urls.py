from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /home/
    url(r'^$', views.HomeView.as_view(), name='overview'),

    # ex: /home/stats/
    url(r'^stats', views.DataListView.as_view(), name='stats'),
]
