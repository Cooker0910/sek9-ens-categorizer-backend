from rest_framework import serializers
from .models import Tag


class TagSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag
    fields = (
      'id',
      'name',
      'priority',
      'description',
      'updated_at',
      'created_at',
    )
    read_only_fields = (
      'id',
      'updated_at',
      'created_at',
    )


class NewTagSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag
    fields = (
      'name',
      'priority',
      'description',
    )
