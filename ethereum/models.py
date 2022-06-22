from operator import mod
from pyexpat import model
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.safestring import mark_safe
from category.models import Category
from domain.models import Domain

class Ethereum(models.Model):
  category = models.ForeignKey(
    Category,
    models.SET_NULL,
    blank=True,
    null=True,
    related_name='category_ethereums',
    db_index=True,
  )
  name = models.CharField(max_length=128, blank=False)
  domain = models.ForeignKey(
    Domain,
    models.SET_NULL,
    blank=True,
    null=True,
    related_name='domain_ethereums',
    db_index=True,
  )
  address = models.CharField(max_length=128, blank=True, null=True, default=None)
  description = models.TextField(blank=True, null=True, default=None)
  created_date = models.DateTimeField(blank=True, null=True, default=None)
  resolver = models.CharField(max_length=128, blank=True, null=True, default=None)
  registrant = models.CharField(max_length=128, blank=True, null=True, default=None)  
  expiry_date = models.DateTimeField(blank=True, null=True, default=None)
  balance = models.DecimalField(max_digits=50, decimal_places=18, blank=True, null=True, default=0.0)
  end_price = models.DecimalField(max_digits=50, decimal_places=18, blank=True, null=True, default=0.0)
  end_date = models.DateTimeField(blank=True, null=True, default=None)
  label_hash = models.CharField(max_length=128, blank=True, null=True, default=None)
  owner = models.CharField(max_length=128, blank=True, null=True, default=None)
  payment_token = models.CharField(max_length=128, blank=True, null=True, default=None)
  last_sale = models.DecimalField(max_digits=50, decimal_places=18, blank=True, null=True, default=0.0)
  registration_date = models.DateTimeField(blank=True, null=True, default=None)
  starting_price = models.DecimalField(max_digits=50, decimal_places=18, blank=True, null=True, default=0.0)
  width = models.PositiveIntegerField(blank=True, null=True, default=0)
  views = models.PositiveIntegerField(blank=True, null=True, default=0)
  data = models.TextField(blank=False, default="{}")
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    managed = True
    db_table = 'ethereum'
    ordering = ('category', 'name', 'domain',)
    unique_together = ('name', 'domain')

  def __str__(self):
    return f"{self.name}.{self.domain}"
  
  def eth_name(self):
    return f"{self.name}.{self.domain.name}"
