
import logging
import json
from django.core.management.base import BaseCommand, CommandError
from category.models import Category
from decimal import Decimal

logger = logging.getLogger(__name__)

class Command(BaseCommand):
  help = "repair_category_with_json"

  def add_arguments(self, parser):
      parser.add_argument('--name', nargs='+', type=str)
  
  def get_value(self, data, key, default=None, type=None):
    if key in data.keys():
      return data[key]
    return default if default else None

  def handle(self, *args, **options):
    logger.info("Starting to repaire category...")
    if options['name'] and len(options['name']) > 0:
      file_name = options['name'][0]
      f = open(file_name)
      data = json.load(f)
      categories = data['categories']
      for cat_key in categories:
        print('==== cat: ', cat_key)
        print('==== value: ', categories[cat_key])
        cat_value = categories[cat_key]
        files = self.get_value(cat_value, 'files', None)
        if files:
          files = json.dumps(files)
        floor = round(Decimal(cat_value.get('floorprice_decimal', 0)) / pow(10, 18), 18)
        new_values = {
          'short_name': cat_value.get('shortName', cat_value['name']),
          'description': cat_value.get('description', None),
          'floor': floor,
          'owners': cat_value.get('owners', 0),
          'available': cat_value.get('available', 0),
          'count': cat_value.get('count', 0),
          'image_url': cat_value.get('imageUrl', None),
          'regular_expression': cat_value.get('regularExpression', None),
          'files': files,
          'wiki_url': cat_value.get('wikiUrl', None),
          'community_discord': cat_value.get('communityDiscord', None),
          'community_twitter': cat_value.get('communityTwitter', None),
          'data': json.dumps(cat_value)
        }
        Category.objects.update_or_create(
          name=cat_value['name'],
          defaults=new_values
        )
      
    else:
      print('==== use --name argument.')
    
    logger.info(" Command shut down successfully!")
