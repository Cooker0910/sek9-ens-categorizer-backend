from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Member
from .push_token.admin import *

@admin.register(Member)
class MemberAdmin(ImportExportModelAdmin):
  fields = (
    'id',
    'image',
    'image_tag',
    'email',
    'type',
    'first_name',
    'last_name',
    'sex',
    'telnumber',
    'birth_date',
    'password',
    'active_notification',
    'permanent_discount',
    'confirmed',
    'plat_form',
    'udid',
    'login_date',
    'banned',
    'banned_date',
    'new_email',
    'new_password',
    'updated_at',
    'created_at',
  )
  lds = list(fields)
  lds.remove('image')
  lds.remove('password')
  lds.remove('new_email')
  lds.remove('new_password')
  
  list_display = lds
  readonly_fields = [
    'id',
    'image_tag',
    'updated_at',
    'created_at',
  ]
  list_display_links = list_display
  list_per_page = 25
  sfs = list(list_display)
  sfs.remove('image_tag')
  search_fields = sfs
