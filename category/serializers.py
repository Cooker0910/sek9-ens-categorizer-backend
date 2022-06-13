from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = (
      'id',
      'name',
      'data',
      'updated_at',
      'created_at',
    )
    read_only_fields = (
      'id',
      'updated_at',
      'created_at',
    )


class NewCategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = (
      'name',
      'data',
    )

class CategoryScanFromFileSerializer(serializers.Serializer):
  name = serializers.CharField(required=True)
  uid = serializers.CharField(required=True)
  file_url = serializers.CharField(required=True)

