from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.safestring import mark_safe

class Category(models.Model):
  name = models.CharField(max_length=128, blank=False)
  short_name = models.CharField(max_length=128, blank=True, null=True, default="")
  description = models.TextField(blank=True, null=True, default=None)
  floor = models.DecimalField(max_digits=50, decimal_places=18, blank=True, null=True, default=0.0)
  owners = models.PositiveIntegerField(blank=True, null=True, default=0)
  available = models.PositiveIntegerField(blank=True, null=True, default=0)
  count = models.PositiveIntegerField(blank=True, null=True, default=0)
  image_url = models.CharField(max_length=1024, blank=True, null=True, default=None)
  regular_expression = models.CharField(max_length=256, blank=True, null=True, default=None)
  files = models.JSONField(max_length=1024, blank=True, null=True, default=None)
  wiki_url = models.CharField(max_length=256, blank=True, null=True, default=None)
  community_discord = models.CharField(max_length=256, blank=True, null=True, default=None)
  community_twitter = models.CharField(max_length=256, blank=True, null=True, default=None)
  data = models.TextField(blank=False, default="{}")
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    managed = True
    db_table = 'category'
    ordering = ('name',)
    unique_together = ('name',)

  def __str__(self):
    return self.name
  
  def tags(self):
    res = []
    cts = self.ct_categories.all()
    for ct in cts:
      res.append(ct.tag.name)
    return res
