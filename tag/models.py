from operator import mod
from pyexpat import model
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.safestring import mark_safe

class Tag(models.Model):
  name = models.CharField(max_length=128, blank=False)
  priority = models.IntegerField(blank=True, null=True, default=1)
  description = models.TextField(blank=True, null=True, default=None)
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    managed = True
    db_table = 'tag'
    ordering = ('priority',)
    unique_together = ('name',)

  def __str__(self):
    return self.name
