from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from author.views import WelcomeView

urlpatterns = patterns('',
    url(r'^login/$', auth_views.login, {'template_name':'login.html'}),
    url('^', include('django.contrib.auth.urls')),
    url(r'^$',  WelcomeView.as_view(), name="welcome"),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^surveys/', include("survey.urls", namespace='survey')),

)
