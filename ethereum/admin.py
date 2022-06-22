from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Ethereum

@admin.register(Ethereum)
class EthereumAdmin(ImportExportModelAdmin):
  fields = (
    'id',
    'category',
    'name',
    'domain',
    'address',
    'balance',
    'owner',
    'description',
    'created_date',
    'registration_date',
    'resolver',
    'registrant',
    'expiry_date',
    'starting_price',
    'end_price',
    'end_date',
    'label_hash',
    'payment_token',
    'last_sale',
    'width',
    'data',
    'updated_at',
    'created_at',
  )
  lds = list(fields)
  lds.remove('end_date')
  lds.remove('label_hash')
  lds.remove('payment_token')
  lds.remove('last_sale')
  lds.remove('width')
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
  sfs.remove('category')
  sfs.remove('domain')
  search_fields = sfs
