"""jb  URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    #url(r'^testbook/$','jbapi.views.testbook'),
    url(r'^sign_up_and_list_users/$','jbapi.views.sign_up_and_list_users'),
    url(r'^perform_exchange/$','jbapi.views.perform_exchange'),
    url(r'^perform_exchange/$','jbapi.views.perform_exchange'),
    url(r'^books/$','jbapi.views.listbooks'),
    url(r'^addbook/$','jbapi.views.addbook'),
    url(r'^searchbook/$','jbapi.views.searchbook'),
    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^', include('jbapi.urls')),
    #url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^backend_auth/$','jbapi.views.authenticating'),
]
