from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.safestring import mark_safe
from utils.string_utils import Truncate_Text

class Newsletter(models.Model):
  subject = models.CharField( max_length=128, blank=False)
  message = models.TextField(blank=False)
  is_sent = models.BooleanField(blank=True, null=True, default=False)
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    managed = True
    db_table = 'newsletter'
    ordering = ('-id',)
    unique_together = ('id',)

  def __str__(self):
    return f"{str(self.created_at)}: {Truncate_Text(self.subject, 10)} : {Truncate_Text(self.message)}"