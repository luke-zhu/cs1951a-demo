from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^reddit', views.reddit, name='reddit'),
    url(r'^genius', views.genius, name='genius'),
]