from operator import mod
from pyexpat import model
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.safestring import mark_safe
from member.models import Member
from ethereum.models import Ethereum

class Favorit(models.Model):
  member = models.ForeignKey(
    Member,
    models.SET_NULL,
    blank=True,
    null=True,
    related_name='member_favorits',
    db_index=True,
  )
  ethereum = models.ForeignKey(
    Ethereum,
    models.SET_NULL,
    blank=True,
    null=True,
    related_name='ethereum_favorits',
    db_index=True,
  )
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    managed = True
    db_table = 'favorit'
    ordering = ('member', 'ethereum')
    unique_together = ('member', 'ethereum')

  def __str__(self):
    return f"{self.member.full_name()}: {self.member.email}: {self.ethereum.eth_name()}"

