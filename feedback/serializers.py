from rest_framework import serializers
from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
  class Meta:
    model = Feedback
    fields = (
      'id',
      'sender',
      'message',
      'updated_at',
      'created_at',
    )
    read_only_fields = (
      'id',
      'updated_at',
      'created_at',
    )


class NewFeedbackSerializer(serializers.ModelSerializer):
  class Meta:
    model = Feedback
    fields = (
      'sender',
      'message',
    )
