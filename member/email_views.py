import os
import json
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.shortcuts import render
from django.conf import settings
from utils.email_utils import (
  get_member_password_email_context
)
from .models import Member


def password_email_viewer(request, pk):
  member = Member.objects.get(pk=pk)
  template = settings.EMAIL_PASSWORD_GENERATE_MAIL_HTML
  context = get_member_password_email_context(member)
  return render(
    request,
    template,
    context
  )
