from rest_framework import serializers
from .models import Ethereum
from category.serializers import CategorySerializer
from domain.serializers import DomainSerializer

class EthereumSerializer(serializers.ModelSerializer):
  class Meta:
    model = Ethereum
    fields = (
      'id',
      'category',
      'name',
      'domain',
      'eth_name',
      'address',
      'owner',
      'description',
      'created_date',
      'resolver',
      'registrant',
      'registration_date',
      'expiry_date',
      'balance',
      'starting_price',
      'end_price',
      'end_date',
      'label_hash',
      'payment_token',
      'last_sale',
      'width',
      'views',
      'updated_at',
      'created_at',
    )
    read_only_fields = (
      'id',
      'updated_at',
      'created_at',
    )


class EthereumFullSerializer(serializers.ModelSerializer):
  category = CategorySerializer(required=False, many=False)
  domain = DomainSerializer(required=False, many=False)
  class Meta:
    model = Ethereum
    fields = (
      'id',
      'category',
      'name',
      'domain',
      'eth_name',
      'address',
      'owner',
      'owners',
      'description',
      'created_date',
      'resolver',
      'registrant',
      'registration_date',
      'expiry_date',
      'balance',
      'starting_price',
      'end_price',
      'end_date',
      'label_hash',
      'payment_token',
      'last_sale',
      'width',
      'views',
      'updated_at',
      'created_at',
    )
    read_only_fields = (
      'id',
      'updated_at',
      'created_at',
    )


class NewEthereumSerializer(serializers.ModelSerializer):
  class Meta:
    model = Ethereum
    fields = (
      'category',
      'name',
      'domain',
      'address',
      'owner',
      'owners',
      'description',
      'created_date',
      'resolver',
      'registrant',
      'registration_date',
      'expiry_date',
      'balance',
      'starting_price',
      'end_price',
      'end_date',
      'label_hash',
      'payment_token',
      'last_sale',
      'width',
      'views',
    )

class EthereumScanSerializer(serializers.Serializer):
  name = serializers.CharField(required=True)
  uid = serializers.CharField(required=True)
  file_url = serializers.CharField(required=True)

