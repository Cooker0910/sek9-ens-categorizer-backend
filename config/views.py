from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def api_home(request):
  return redirect('/apis')

def error404(request, exception):
  return redirect('/super-admin')
