
import logging
from django.core.management.base import BaseCommand, CommandError
from utils.category_utils import scan_category_by_re

logger = logging.getLogger(__name__)


class Command(BaseCommand):
  help = "category"

  def add_arguments(self, parser):
      parser.add_argument('--name', nargs='+', type=str)

  def handle(self, *args, **options):
    logger.info("Starting to scan the ETH domain names in category by Regular Expression...")
    if options['name'] and len(options['name']) > 0:
      for cat_name in options['name']:
        try:
          print('==== category name: ', cat_name)
          res = scan_category_by_re(cat_name)
          print('===== result: ', res)
        except Exception as e:
          raise CommandError(f'Scan "{cat_name}" was failed: {e}')
    else:
      print('==== use --name argument.')
    
    logger.info(" Command shut down successfully!")
