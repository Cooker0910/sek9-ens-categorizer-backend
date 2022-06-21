import json
from ntpath import join
import time
from django.utils.timezone import now
from django.shortcuts import render
from django.db import connection, transaction
from django.db import models
from django.db.models import Q, Sum, Max, Count
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
import member
from utils.string_utils import str2bool
from utils.pagination_utils import (
  FilterPagination,
)
from .models import Ethereum
from .serializers import (
  EthereumSerializer,
  NewEthereumSerializer,
  EthereumScanSerializer
)
from domain.models import Domain
from utils.ens_utils import scan_ens
import logging

logger = logging.getLogger(__name__)

def join_two_queries(first_query, second_query):
  res = first_query
  if second_query:
    if res:
      res = res & second_query
    else:
      res = second_query
  return res

class EthereumList(APIView):
  permission_classes = []
  domain_param = openapi.Parameter(
    'domain_name',
    openapi.IN_QUERY,
    description='Name of domain.',
    type=openapi.TYPE_STRING
  )
  category_id_param = openapi.Parameter(
    'category_id',
    openapi.IN_QUERY,
    description='ID of category.',
    type=openapi.TYPE_INTEGER
  )
  paramenters = [domain_param, category_id_param,] + FilterPagination.generate_pagination_params()

  @swagger_auto_schema(
    manual_parameters=paramenters,
    responses={200: EthereumSerializer(many=True)}
  )
  def get(self, request, format=None):
    domain_name = request.GET.get('domain_name', None)
    category_id = request.GET.get('category_id', None)
    queries = None
    domain_query = None
    category_query = None
    if domain_name:
      d = Domain.objects.filter(name=domain_name).first
      if d:
        domain_query = Q(domain=d)
    if category_id:
      category_query = Q(category_id=category_id)
    queries = join_two_queries(domain_query, category_query)
    print('==== queries: ', queries)
    resultset = FilterPagination.get_paniation_data(
      request,
      Ethereum,
      EthereumSerializer,
      queries=queries,
      order_by_array=('name',)
    )
    return Response(resultset)


class EthereumListByCategoryId(APIView):
  permission_classes = []

  @swagger_auto_schema(
    manual_parameters=FilterPagination.generate_pagination_params(),
    responses={200: EthereumSerializer(many=True)}
  )
  def get(self, request, format=None):
    resultset = FilterPagination.get_paniation_data(
      request,
      Ethereum,
      EthereumSerializer,
      queries=None,
      order_by_array=('name',)
    )
    return Response(resultset)


class EthereumDetail(APIView):
  permission_classes = []

  def get_object(self, pk):
    try:
      return Ethereum.objects.get(pk=pk)
    except Ethereum.DoesNotExist:
      raise Http404

  @swagger_auto_schema(
    responses={200: EthereumSerializer(many=False)}
  )
  def get(self, request, pk, format=None):
    item = self.get_object(pk)
    serializer = EthereumSerializer(item)
    return Response(serializer.data, status=status.HTTP_200_OK)

  @swagger_auto_schema(
    request_body=EthereumSerializer(many=False),
    responses={200: EthereumSerializer(many=False)}
  )
  def put(self, request, pk, format=None):
    item = self.get_object(pk)
    serializer = EthereumSerializer(item, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    item = self.get_object(pk)
    # Delete all patients
    item.dentist_patients.all().delete()
    item.delete()
    return Response(status=status.HTTP_200_OK)


class EthereumCreate(APIView):
  permission_classes = []

  @swagger_auto_schema(
      request_body=NewEthereumSerializer(many=False),
      responses={200: EthereumSerializer(many=False)}
  )
  def post(self, request, format=None):
    serializer = NewEthereumSerializer(data=request.data, many=False)
    if serializer.is_valid():
      # Create new member with serializer
      new_item = Ethereum.objects.create(**serializer.validated_data)
      new_serializer = EthereumSerializer(new_item, many=False)
      return Response(new_serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class EthereumScan(APIView):
  permission_classes = []

  @swagger_auto_schema(
      request_body=EthereumScanSerializer(many=False),
      responses={200: EthereumSerializer(many=False)}
  )
  def post(self, request, format=None):
    serializer = EthereumScanSerializer(data=request.data, many=False)
    if serializer.is_valid():
      # Download and parse the file.
      # Get each eth names
      eth_name = 'test.eth'
      res = scan_ens(eth_name)
      return Response(data=res, status=status.HTTP_201_CREATED)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

