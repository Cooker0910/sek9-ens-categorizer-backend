from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Category

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
  fields = (
    'id',
    'name',
    'short_name',
    'description',
    'floor',
    'owners',
    'available',
    'count',
    'views',
    'image_url',
    'regular_expression',
    'files',
    'wiki_url',
    'community_discord',
    'community_twitter',
    'data',
    'updated_at',
    'created_at',
  )
  lds = list(fields)
  lds.remove('data')
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
