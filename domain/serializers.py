from rest_framework import serializers
from .models import Domain


class DomainSerializer(serializers.ModelSerializer):
  class Meta:
    model = Domain
    fields = (
      'id',
      'name',
      'description',
      'updated_at',
      'created_at',
    )
    read_only_fields = (
      'id',
      'updated_at',
      'created_at',
    )


class NewDomainSerializer(serializers.ModelSerializer):
  class Meta:
    model = Domain
    fields = (
      'name',
      'description',
    )
