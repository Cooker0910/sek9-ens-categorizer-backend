from django.conf.urls import include
from django.urls import re_path
from . import views, csv_views

urlpatterns = [
  re_path(r'^all/', views.CategoryList.as_view()),
  re_path(r'^create/', views.CategoryCreate.as_view()),
  re_path(r'^newest/', views.CategoryNewest.as_view()),
  re_path(r'^most_viewd/', views.CategoryMostViewd.as_view()),
  re_path(r'^most_purchased/', views.CategoryMostPurchased.as_view()),
  re_path(r'^(?P<pk>[0-9]+)/', views.CategoryDetail.as_view()),
  re_path(r'^scan_from_file/', views.CategoryScanFromFile.as_view()),
]
