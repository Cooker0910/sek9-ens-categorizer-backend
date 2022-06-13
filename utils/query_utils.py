from django.db.models import Q
from member.models import Member

def join_two_queries(first_query, second_query):
  res = first_query
  if second_query:
    if res:
      res = res & second_query
    else:
      res = second_query
  return res

