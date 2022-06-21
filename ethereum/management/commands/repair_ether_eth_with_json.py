
import logging
import json
import pytz
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from category.models import Category
from ethereum.models import Ethereum
from domain.models import Domain
from decimal import Decimal

logger = logging.getLogger(__name__)
tz = pytz.timezone("US/Eastern")

class Command(BaseCommand):
  help = "repair_category_with_json"

  def add_arguments(self, parser):
      parser.add_argument('--name', nargs='+', type=str)
  
  def get_value(self, data, key, default=None, type=None):
    if key in data.keys():
      return data[key]
    return default if default else None
  
  def eth_price_to_decimal(self, price):
    print('==== price: ', price)
    if price is None:
      return 0
    return round(Decimal(price) / pow(10, 18), 18)

  def timestamp_to_datetime(self, ts):
    if ts is None:
      return None
    try:
      return datetime.fromtimestamp(ts, tz)
    except Exception as err:
      print('==== timestamp_to_datetime: ', str(err))
      return None

  def handle(self, *args, **options):
    logger.info("Starting to repaire category...")
    if options['name'] and len(options['name']) > 0:
      file_name = options['name'][0]
      f = open(file_name)
      data = json.load(f)
      domains = data['domains']
      cats = domains['eth']
      for cat_name in cats:
        print('==== cat_name: ', cat_name)
        eths = cats[cat_name]
        for eth_key in eths:
          eth_value = eths[eth_key]
          # print('==== eth_key: ', eth_key)
          # print('==== eth_value: ', eth_value)
          
          category = Category.objects.filter(name=cat_name).first()
          domain = Domain.objects.filter(name='eth').first()
          print('===== category, domain: ', category, domain)
          if (category is None) or (domain is None):
            continue
          new_values = {
            # 'category': category,
            # 'name': eth_value.get('name'),
            # 'domain': domain,
            'address': eth_value.get('labelHash', None),
            'description': eth_value.get('description', None),
            'resolver': eth_value.get('description', None),
            'registrant': eth_value.get('description', None),
            'created_date': self.timestamp_to_datetime(eth_value.get('createdDate', None)),
            'expiry_date': self.timestamp_to_datetime(eth_value.get('expiryDate', None)),
            'end_price': self.eth_price_to_decimal(eth_value.get('endingPrice_decimal', 0)),
            'end_date': self.timestamp_to_datetime(eth_value.get('endDate', None)),
            'label_hash': eth_value.get('labelHash', None),
            'owner': eth_value.get('owner', None),
            'payment_token': eth_value.get('paymentToken', None),
            'last_sale': eth_value.get('lastSale', 0),
            'registration_date': self.timestamp_to_datetime(eth_value.get('registrationDate', None)),
            'starting_price': self.eth_price_to_decimal(eth_value.get('startingPrice_decimal', 0)),
            'width': eth_value.get('width', 0),
            'data': json.dumps(eth_value)
          }
          print('===== new_values: ', new_values)
          try:
            Ethereum.objects.update_or_create(
              category=category,
              name=eth_value['name'],
              domain=domain,
              defaults=new_values
            )
          except Exception as err:
            print('===== Ethereum.objects.update_or_create: ', str(err))
    else:
      print('==== use --name argument.')
    
    logger.info(" Command shut down successfully!")
