from django.db import connection, transaction
from django.db import models
from utils.pagination_utils import FilterPagination
import logging

logger = logging.getLogger(__name__)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def execute_raw_sql(str_sql, params=[], titles=[]):
  try:
    cursor = connection.cursor()
    cursor.execute(str_sql, params)
    # transaction.commit_unless_managed()
    items = []
    if len(titles) == 0:
      items = dictfetchall(cursor)
      return items
    cursor.fetchall()
    new_items = []
    for item in items:
      new_item = {}
      for idx, val in enumerate(titles):
        new_item[val] = item[idx]
      new_items.append(new_item)
    return new_items
  except Exception as e:
    logger.error('Failed to run sql: ' + str_sql, params, titles)
    logger.error('execute_raw_sql: except: ' + str(e))
    return []


def execute_raw_sql_with_pagination(request, str_sql, params=[], titles=[], serializer_class=None):
  items = execute_raw_sql(str_sql, params, titles)
  return FilterPagination.get_paniation_data_by_array(
    request,
    items,
    serializer_class
  )
