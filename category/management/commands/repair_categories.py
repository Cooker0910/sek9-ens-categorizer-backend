
import logging
from django.core.management.base import BaseCommand
from category.models import Category
from utils.category_utils import repaire_category_balance

logger = logging.getLogger(__name__)

class Command(BaseCommand):
  help = "repair_category_with_json"

  def handle(self, *args, **options):
    logger.info("Starting to repaire category...")
    categories = Category.objects.all()
    for cat in categories:
      repaire_category_balance(cat)
    logger.info(" Command shut down successfully!")
