from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
  re_path(r'^login/', views.CustomLogin.as_view()),
  re_path(r'^logout/', views.Logout.as_view()),
  re_path(r'^register/', views.Register.as_view()),
  re_path(r'token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  re_path(r'token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]