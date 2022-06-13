
import logging
from django.core.management.base import BaseCommand, CommandError
from utils.category_utils import scan_category

logger = logging.getLogger(__name__)


class Command(BaseCommand):
  help = "category"

  def add_arguments(self, parser):
      parser.add_argument('--name', nargs='+', type=str)

  def handle(self, *args, **options):
    logger.info("Starting to scan the ETH domain names in category...")
    if options['name'] and len(options['name']) > 0:
      for cat_name in options['name']:
        try:
          res = scan_category(cat_name)
          print('===== name: ', cat_name, res)
        except Exception as e:
          raise CommandError(f'Scan "{cat_name}" was failed: {e}')
    else:
      print('==== use --name argument.')
    
    logger.info(" Command shut down successfully!")
