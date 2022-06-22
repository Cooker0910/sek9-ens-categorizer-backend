from django.conf.urls import include
from django.urls import re_path
from . import views, csv_views

urlpatterns = [
  re_path(r'^all/', views.FavoritList.as_view()),
  re_path(r'^create/', views.FavoritCreate.as_view()),
  re_path(r'^(?P<pk>[0-9]+)/', views.FavoritDetail.as_view()),
]
