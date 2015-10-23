from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from author.views import WelcomeView, LogoutView
from django.views.generic import TemplateView
from .views import login

urlpatterns = patterns('',
    url(r'^surveys/', include("survey.urls", namespace='survey')),
    url(r'^logout/$', LogoutView.as_view()),
    url(r'^login/$', login, {'template_name':'login.html'}),
    url(r'^create/$',  TemplateView.as_view(template_name='create.html'), name='create'),
    url(r'^home/$',  TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^add/$',  TemplateView.as_view(template_name='add.html'), name='add'),
    url(r'^author/$',  TemplateView.as_view(template_name='author.html'), name='author'),
    url(r'^home/$',  TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',  WelcomeView.as_view(), name="welcome"),
    url('^', include('django.contrib.auth.urls')),

)
