from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Domain

@admin.register(Domain)
class DomainAdmin(ImportExportModelAdmin):
  fields = (
    'id',
    'name',
    'description',
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
  search_fields = sfs
