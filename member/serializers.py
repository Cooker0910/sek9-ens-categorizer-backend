from rest_framework import serializers
from .models import Member


class MemberSerializer(serializers.ModelSerializer):
  class Meta:
    model = Member
    fields = (
      'id',
      'image',
      'email',
      'type',
      'first_name',
      'last_name',
      'sex',
      'telnumber',
      'birth_date',
      'password',
      'active_notification',
      'confirmed',
      'plat_form',
      'udid',
      'login_date',
      'banned',
      'banned_date',
      'permanent_discount',
      # 'new_email',
      # 'new_password',
      'updated_at',
      'created_at',
    )
    read_only_fields = (
      'id',
      'type',
      'login_date',
      'banned',
      'banned_date',
      'updated_at',
      'created_at',
    )


class NewMemberSerializer(serializers.ModelSerializer):
  class Meta:
    model = Member
    fields = (
      'image',
      'email',
      'type',
      'first_name',
      'last_name',
      'sex',
      'telnumber',
      'birth_date',
      'password',
      'active_notification',
      'permanent_discount',
      'plat_form',
      'udid',
    )
