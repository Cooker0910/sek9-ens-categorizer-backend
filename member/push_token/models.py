from django.db import models
from django.utils.safestring import mark_safe
from member.models import Member

class PushToken(models.Model):
  PLATFOM_WEB = 'WEB'
  PLATFOM_IPHONE = 'IPHONE'
  PLATFOM_ANDROID = 'ANDROID'
  PLATFOM_TYPE = (
    (PLATFOM_WEB, PLATFOM_WEB),
    (PLATFOM_IPHONE, PLATFOM_IPHONE),
    (PLATFOM_ANDROID, PLATFOM_ANDROID),
  )

  member = models.ForeignKey(
    Member,
    on_delete=models.CASCADE,
    blank=False,
    related_name='member_push_tokens'
  )
  plat_form = models.CharField(choices=PLATFOM_TYPE, max_length=10, blank=True, default=PLATFOM_WEB)
  player_id = models.CharField(max_length=256, blank=True, null=True)
  udid = models.CharField(max_length=64, blank=True, null=True)
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    managed = True
    db_table = 'push_token'
    ordering = ('-id',)
    unique_together = ('member', 'plat_form',)

  def __str__(self):
    res = str(self.id)
    if self.member:
      res = res + ': ' + str(self.member)
    if self.plat_form:
      res = res + ' ' + self.plat_form
    return res
