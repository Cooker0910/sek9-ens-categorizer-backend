from rest_framework import serializers
from .models import CategoryTag


class CategoryTagSerializer(serializers.ModelSerializer):
  class Meta:
    model = CategoryTag
    fields = (
      'id',
      'category',
      'tag',
      'description',
      'updated_at',
      'created_at',
    )
    read_only_fields = (
      'id',
      'updated_at',
      'created_at',
    )


class NewCategoryTagSerializer(serializers.ModelSerializer):
  class Meta:
    model = CategoryTag
    fields = (
      'category',
      'tag',
      'description',
    )

