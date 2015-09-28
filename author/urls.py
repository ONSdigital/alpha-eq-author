from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from author.views import WelcomeView
from django.views.generic import TemplateView

urlpatterns = patterns('',
<<<<<<< HEAD
    url(r'^create/$',  TemplateView.as_view(template_name='create.html'), name='create'),
    url(r'^add/$',  TemplateView.as_view(template_name='add.html'), name='add'),
    url(r'^$',  TemplateView.as_view(template_name='index.html'), name='home'),
=======
    url(r'^login/$', auth_views.login, {'template_name':'login.html'}),
    url('^', include('django.contrib.auth.urls')),
    url(r'^$',  WelcomeView.as_view(), name="welcome"),

    url(r'^create/$',  TemplateView.as_view(template_name='create.html'), name='create'),
    url(r'^home/$',  TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^add/$',  TemplateView.as_view(template_name='add.html'), name='add'),
    url(r'^home/$',  TemplateView.as_view(template_name='index.html'), name='home'),
>>>>>>> 2fed29bb3ba6412f0ba9de901f1b468ff22a8792
    url(r'^admin/', include(admin.site.urls)),
    url(r'^surveys/', include("survey.urls", namespace='survey')),

)
