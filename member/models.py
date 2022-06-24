from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.safestring import mark_safe

class Member(models.Model):
  SEX_MALE = 'male'
  SEX_FEMALE = 'female'
  SEX_CHOICE = (
    (SEX_MALE, SEX_MALE),
    (SEX_FEMALE, SEX_FEMALE),
  )

  ADMIN = 'ADMIN'
  USER = 'USER'
  MEMBER_TYPE = (
    (ADMIN, ADMIN),
    (USER, USER),
  )

  PLATFOM_WEB = 'WEB'
  PLATFOM_IPHONE = 'IPHONE'
  PLATFOM_ANDROID = 'ANDROID'
  PLATFOM_TYPE = (
    (PLATFOM_WEB, PLATFOM_WEB),
    (PLATFOM_IPHONE, PLATFOM_IPHONE),
    (PLATFOM_ANDROID, PLATFOM_ANDROID),
  )

  email = models.CharField(max_length=60, blank=False)
  type = models.CharField(choices=MEMBER_TYPE, max_length=15, blank=False)
  first_name = models.CharField(max_length=128, blank=False)
  last_name = models.CharField(max_length=128, blank=False)
  sex = models.CharField(choices=SEX_CHOICE, max_length=10, blank=True, null=True, default=None)
  telnumber = models.CharField(max_length=40, blank=True, null=True, default=None)
  birth_date = models.DateField(blank=True, null=True, default=None)
  image = models.CharField(max_length=1024, blank=True, null=True, default=None)
  password = models.CharField(max_length=128, blank=False, validators=[MinLengthValidator(6)])
  active_notification = models.BooleanField(blank=False, default=True)
  confirmed = models.BooleanField(blank=False, default=False)
  plat_form = models.CharField(choices=PLATFOM_TYPE, max_length=10, blank=True, default=PLATFOM_WEB)
  udid = models.CharField(max_length=64, blank=True, null=True)
  login_date = models.DateTimeField(blank=True, null=True)
  banned = models.BooleanField(blank=True, default=False)
  banned_date = models.DateTimeField(blank=True, null=True)
  new_email = models.CharField(max_length=60, blank=True, null=True)
  new_password = models.CharField(max_length=128, blank=True, null=True)
  permanent_discount = models.FloatField(blank=True, null=True, default=None)
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    managed = True
    db_table = 'member'
    ordering = ('-id',)
    unique_together = ('email', 'type',)

  def __str__(self):
    res = str(self.id)
    if self.first_name:
      res = res + ': ' + self.first_name
    if self.last_name:
      res = res + ' ' + self.last_name
    if self.type:
      res = res + ' (' + self.type + ')'
    return res

  def image_tag(self):
    res = None
    if self.image:
      res = mark_safe('<img src="{src}" width="{width}" />'
        .format(
            src=self.image if self.image else '',
            width=80,
            height='auto'
        ))
    return res

  def full_name(self):
    res = ''
    if self.first_name:
      res = res + self.first_name
    if self.last_name:
      res = res + ' ' + self.last_name
    return res
