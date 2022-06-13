from django.conf.urls import include
from django.urls import re_path
from . import views, csv_views, email_views

urlpatterns = [
  re_path(r'^all/', views.MemberList.as_view()),
  re_path(r'^create/', views.MemberCreate.as_view()),
  re_path(r'^(?P<pk>[0-9]+)/password_email_viewer/', email_views.password_email_viewer, name="member_password_email_viewer"),
  re_path(r'^(?P<pk>[0-9]+)/', views.MemberDetail.as_view()),
]
