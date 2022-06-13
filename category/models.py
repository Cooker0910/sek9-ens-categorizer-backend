from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.safestring import mark_safe

class Category(models.Model):
  name = models.CharField(max_length=128, blank=False)
  data = models.TextField(blank=False, default="{}")
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    managed = True
    db_table = 'category'
    ordering = ('-id',)
    unique_together = ('name',)

  def __str__(self):
    return self.name
