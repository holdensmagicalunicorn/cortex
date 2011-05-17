from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to

from chat.views import (
        home,
        users,
        socketio
)

from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

    # A list of chatrooms
    url(
        regex=r'^$',
        view=home,
        name='home'
    ),

    # Socket IO hook
    url(
        regex=r'^socket\.io',
        view=socketio,
        name='socketio'
    ),

    url(
        r'^admin/',
        include(admin.site.urls)
    ),

    #url(
    #    r'^users/',
    #    view=users,
    #    name='users'
    #),

   ('^users/login/$', redirect_to, {'url': '/admin'})
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
