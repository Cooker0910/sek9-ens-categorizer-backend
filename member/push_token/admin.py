from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import PushToken

@admin.register(PushToken)
class PushTokenAdmin(ImportExportModelAdmin):
  fields = (
    'id',
    'member',
    'plat_form',
    'udid',
    'player_id',
    'updated_at',
    'created_at',
  )
  sfs = list(fields)
  
  list_display = sfs
  readonly_fields = [
    'id',
    'updated_at',
    'created_at',
  ]
  list_display_links = list_display
  list_per_page = 25
  search_fields = list_display
