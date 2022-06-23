from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.safestring import mark_safe
from utils.string_utils import Truncate_Text

class Feedback(models.Model):
  sender = models.CharField(max_length=128, blank=False)
  message = models.TextField(blank=False)
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    managed = True
    db_table = 'feedback'
    ordering = ('-id',)
    unique_together = ('id',)

  def __str__(self):
    res = str(self.email)
    if self.message:
      res = res + ': ' + Truncate_Text(self.message)
    return res
