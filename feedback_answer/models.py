from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.safestring import mark_safe
from utils.string_utils import Truncate_Text
from feedback.models import Feedback

class FeedbackAnswer(models.Model):
  feedback = models.ForeignKey(
    Feedback,
    models.SET_NULL,
    blank=True,
    null=True,
    related_name='feedback_fbanswers',
    db_index=True,
  )
  message = models.TextField(blank=False)
  is_sent = models.BooleanField(blank=True, null=True, default=False)
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    managed = True
    db_table = 'feedback_answers'
    ordering = ('-id',)
    unique_together = ('id',)

  def __str__(self):
    return f"{str(self.feedback)}: {Truncate_Text(self.message)}"