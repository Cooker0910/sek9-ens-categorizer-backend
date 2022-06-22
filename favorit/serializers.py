from rest_framework import serializers
from .models import Favorit
from ethereum.serializers import EthereumFullSerializer


class FavoritSerializer(serializers.ModelSerializer):
  ethereum = EthereumFullSerializer(required=True, many=False)
  class Meta:
    model = Favorit
    fields = (
      'id',
      'member',
      'ethereum',
      'updated_at',
      'created_at',
    )
    read_only_fields = (
      'id',
      'updated_at',
      'created_at',
    )


class NewFavoritSerializer(serializers.ModelSerializer):
  class Meta:
    model = Favorit
    fields = (
      'member',
      'ethereum',
    )
