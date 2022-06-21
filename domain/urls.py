from django.conf.urls import include
from django.urls import re_path
from . import views, csv_views

urlpatterns = [
  re_path(r'^all/', views.DomainList.as_view()),
  re_path(r'^create/', views.DomainCreate.as_view()),
  re_path(r'^(?P<pk>[0-9]+)/', views.DomainDetail.as_view()),
]
