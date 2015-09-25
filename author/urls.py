from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView



urlpatterns = patterns('',
    url(r'^create/$',  TemplateView.as_view(template_name='create.html'), name='create'),
    url(r'^add/$',  TemplateView.as_view(template_name='add.html'), name='add'),
    url(r'^$',  TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^admin/', include(admin.site.urls)),
)
