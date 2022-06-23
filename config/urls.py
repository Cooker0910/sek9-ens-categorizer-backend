import os
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.urls import re_path
from django.conf.urls.static import static, serve
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_swagger.views import get_swagger_view
from rest_framework import permissions
from rest_framework.authtoken import views
from .views import api_home
from email_verification import urls as email_urls
from email_verification import forget_password_urls
from email_verification import change_user_info_urls
from django.conf.urls import (
  handler400, handler403, handler404, handler500)
from .views import error404

handler404 = error404

swagger_schema_view = get_swagger_view(
    title='SEK9 API',
    url=os.environ.get('SWAGGER_BASE_URL', 'http://www.sek9.com/'),
    urlconf=os.environ.get('SWAGGER_BASE_URL', 'http://www.sek9.com/'),
)

schema_view = get_schema_view(
   openapi.Info(
      title="SEK9 API",
      default_version='v1',
      description="REST API for SEK9 backend application",
      terms_of_service=os.environ.get('SWAGGER_BASE_URL', 'http://www.sek9.com/') + 'termsofservice',
      contact=openapi.Contact(email="contact@sek9.com"),
      license=openapi.License(name="www.sek9.com"),
   ),
   # validators=['flex', 'ssv'],
   public=True,
   permission_classes=(permissions.AllowAny,),
)

def trigger_error(request):
  division_by_zero = 1 / 0

urlpatterns = [
    # Admin URL
    path('super-admin/', admin.site.urls),
    re_path(r'^_nested_admin/', include('nested_admin.urls')),
    # Auth URL
    # path('email/', include(email_urls)),
    # path('forget_password/', include(forget_password_urls)),
    # path('change_user_info/', include(change_user_info_urls)),
    # API urls
    re_path(r'^apis(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^apis/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^api-docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Authentication
    re_path(r'^api/v1/auth/', include('authentication.urls')),
    # S3 upload url
    # re_path(r'^s3direct/', include('s3direct.urls')),
    # Members
    # re_path(r'^api/v1/member/', include('member.urls')),
    re_path(r'^api/v1/category/', include('category.urls')),
    re_path(r'^api/v1/tag/', include('tag.urls')),
    re_path(r'^api/v1/domain/', include('domain.urls')),
    re_path(r'^api/v1/ethereum/', include('ethereum.urls')),
    re_path(r'^api/v1/category_tag/', include('category_tag.urls')),
    re_path(r'^api/v1/favorit/', include('favorit.urls')),
    re_path(r'^api/v1/newsletter/', include('newsletter.urls')),
    re_path(r'^api/v1/feedback/', include('feedback.urls')),
    re_path(r'^api/v1/feedback_answer/', include('feedback_answer.urls')),
    # Default url
    re_path(r'^$', api_home, name='api_home'),
]
