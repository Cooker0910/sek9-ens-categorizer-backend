
import logging
from django.core.management.base import BaseCommand, CommandError
from utils.ens_utils import scan_ens

logger = logging.getLogger(__name__)


class Command(BaseCommand):
  help = "scan_ens"

  def add_arguments(self, parser):
      parser.add_argument('--name', nargs='+', type=str)

  def handle(self, *args, **options):
    logger.info("Starting to scan the ETH domain names...")
    if options['name'] and len(options['name']) > 0:
      for eth_name in options['name']:
        try:
          res = scan_ens(eth_name)
          print('===== name: ', eth_name, res)
        except Exception as e:
          raise CommandError(f'Scan "{eth_name}" was failed: {e}')
    else:
      print('==== use --name argument.')
    
    logger.info(" Command shut down successfully!")
