from operator import mod
from pyexpat import model
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.safestring import mark_safe
from category.models import Category
from tag.models import Tag

class CategoryTag(models.Model):
  category = models.ForeignKey(
    Category,
    models.SET_NULL,
    blank=True,
    null=True,
    related_name='ct_categories',
    db_index=True,
  )
  tag = models.ForeignKey(
    Tag,
    models.SET_NULL,
    blank=True,
    null=True,
    related_name='ct_tags',
    db_index=True,
  )
  description = models.TextField(blank=True, null=True, default=None)
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    managed = True
    db_table = 'category_tag'
    ordering = ('tag', 'category',)
    unique_together = ('tag', 'category')

  def __str__(self):
    return f"{self.tag}: {self.category}"
