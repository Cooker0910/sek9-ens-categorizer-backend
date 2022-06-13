from django.urls import re_path
from . import views, csv_views

urlpatterns = [
  re_path(r'^all/', views.PushTokenList.as_view()),
  re_path(r'^create/', views.PushTokenCreate.as_view()),
  re_path(r'^export_csv/', csv_views.ExportCsv.as_view()),
  re_path(r'^(?P<pk>[0-9]+)/', views.PushTokenDetail.as_view()),
]