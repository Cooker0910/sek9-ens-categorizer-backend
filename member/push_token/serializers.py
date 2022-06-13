from rest_framework import serializers
from .models import PushToken


class PushTokenSerializer(serializers.ModelSerializer):
  class Meta:
    model = PushToken
    fields = (
      'id',
      'member',
      'plat_form',
      'udid',
      'player_id',
      'updated_at',
      'created_at',
    )
    read_only_fields = (
      'id',
      'updated_at',
      'created_at',
    )


class NewPushTokenSerializer(serializers.ModelSerializer):
  class Meta:
    model = PushToken
    fields = (
      'member',
      'plat_form',
      'udid',
      'player_id',
    )
