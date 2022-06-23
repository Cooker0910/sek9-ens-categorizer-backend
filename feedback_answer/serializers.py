from rest_framework import serializers
from .models import FeedbackAnswer
from feedback.serializers import FeedbackSerializer

class FeedbackAnswerSerializer(serializers.ModelSerializer):
  feedback = FeedbackSerializer(required=True, many=False)
  class Meta:
    model = FeedbackAnswer
    fields = (
      'id',
      'feedback',
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


class NewFeedbackAnswerSerializer(serializers.ModelSerializer):
  class Meta:
    model = FeedbackAnswer
    fields = (
      'feedback',
      'message',
      'is_sent',
    )
