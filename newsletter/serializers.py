from rest_framework import serializers
from .models import Newsletter


class NewsletterSerializer(serializers.ModelSerializer):
  class Meta:
    model = Newsletter
    fields = (
      'id',
      'subject',
      'message',
      'is_sent',
      'updated_at',
      'created_at',
    )
    read_only_fields = (
      'id',
      'updated_at',
      'created_at',
    )


class NewNewsletterSerializer(serializers.ModelSerializer):
  class Meta:
    model = Newsletter
    fields = (
      'subject',
      'message',
    )
