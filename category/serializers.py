from rest_framework import serializers
from .models import Category
# from category_tag.serializers import CategoryTagSerializer
from tag.serializers import TagSerializer

class CategorySerializer(serializers.ModelSerializer):
  # tags = TagSerializer(required=False, many=True)
  class Meta:
    model = Category
    fields = (
      'id',
      'name',
      'short_name',
      'description',
      'floor',
      'owners',
      'available',
      'count',
      'image_url',
      'regular_expression',
      'files',
      'wiki_url',
      'community_discord',
      'community_twitter',
      'tags',
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
      'short_name',
      'description',
      'floor',
      'owners',
      'available',
      'count',
      'image_url',
      'regular_expression',
      'files',
      'wiki_url',
      'community_discord',
      'community_twitter',
    )

class CategoryScanFromFileSerializer(serializers.Serializer):
  name = serializers.CharField(required=True)
  uid = serializers.CharField(required=True)
  file_url = serializers.CharField(required=True)

