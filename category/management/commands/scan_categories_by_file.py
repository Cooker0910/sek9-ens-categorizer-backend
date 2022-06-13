
import logging
from django.core.management.base import BaseCommand, CommandError
from utils.category_utils import scan_categories

logger = logging.getLogger(__name__)


class Command(BaseCommand):
  help = "scan_categories_by_file"

  def handle(self, *args, **options):
    logger.info("Starting to scan the ETH domain names in category...")
    scan_categories()
    
    logger.info(" Command shut down successfully!")
