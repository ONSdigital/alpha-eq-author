from django.conf.urls import patterns, include, url
from django.contrib import admin
from author.views import LoginView, WelcomeView


urlpatterns = patterns('',
    url(r'^login', LoginView.as_view(), name='login'),

    url(r'^$',  WelcomeView.as_view(), name="welcome"),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^surveys/', include("survey.urls", namespace='survey')),

    url(r'^logout', LogoutView.as_view(), name='logout')
)
