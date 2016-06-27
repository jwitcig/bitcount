from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /login/
    url(r'^$', views.LoginView.as_view(), name='login'),

    # ex: /login/authenticate/
    url(r'^authenticate/$', views.AuthenticateView.as_view(), name='authenticate'),

    # ex: /login/callback/
    url(r'^callback/$', views.LoginCallback.as_view(), name='callback'),

    # ex: /login/success/
    url(r'^success/$', views.LoginSuccessView.as_view(), name='success'),
]
