from django.conf.urls import url
from jbapi import views

urlpatterns = [
  url(r'^books/$',views.testbook),
]  