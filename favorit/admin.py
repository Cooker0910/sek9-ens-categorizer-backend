from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Favorit

@admin.register(Favorit)
class FavoritAdmin(ImportExportModelAdmin):
  fields = (
    'id',
    'member',
    'ethereum',
    'updated_at',
    'created_at',
  )
  lds = list(fields)
  list_display = lds
  readonly_fields = [
    'id',
    'updated_at',
    'created_at',
  ]
  list_display_links = list_display
  list_per_page = 25
  sfs = list(list_display)
  sfs.remove('member')
  sfs.remove('ethereum')
  search_fields = sfs
