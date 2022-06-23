
import logging
from django.core.management.base import BaseCommand, CommandError
from utils.category_utils import scan_category_by_id

logger = logging.getLogger(__name__)


class Command(BaseCommand):
  help = "category"

  def add_arguments(self, parser):
      parser.add_argument('--id', nargs='+', type=str)

  def handle(self, *args, **options):
    logger.info("Starting to scan the ETH domain names in category...")
    if options['id'] and len(options['id']) > 0:
      for cat_id in options['id']:
        try:
          res = scan_category_by_id(cat_id)
          print('===== id: ', cat_id, res)
        except Exception as e:
          raise CommandError(f'Scan "{cat_id}" was failed: {e}')
    else:
      print('==== use --name argument.')
    
    logger.info(" Command shut down successfully!")
