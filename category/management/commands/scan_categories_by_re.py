
import logging
from django.core.management.base import BaseCommand, CommandError
from utils.category_utils import scan_categories_by_re

logger = logging.getLogger(__name__)


class Command(BaseCommand):
  help = "scan_categories"

  def handle(self, *args, **options):
    logger.info("Starting to scan the ETH domain names in category by Regular Expression...")
    scan_categories_by_re()
    
    logger.info(" Command shut down successfully!")
