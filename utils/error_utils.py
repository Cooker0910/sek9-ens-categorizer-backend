# custom handler
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
  response = exception_handler(exc, context)
  print('==== error: ', exc, context)
  return response