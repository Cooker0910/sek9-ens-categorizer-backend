from gettext import Catalog
import json
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
from .models import Category
from .serializers import (
  CategorySerializer,
  NewCategorySerializer,
  CategoryScanFromFileSerializer
)
from category_tag.models import CategoryTag
from tag.models import Tag
from utils.ens_utils import scan_ens
import logging

logger = logging.getLogger(__name__)

class CategoryList(APIView):
  permission_classes = []
  tag_param = openapi.Parameter(
    'tag_param',
    openapi.IN_QUERY,
    description='Tag name.',
    type=openapi.TYPE_STRING
  )
  paramenters = [tag_param,] + FilterPagination.generate_pagination_params()

  @swagger_auto_schema(
    manual_parameters=paramenters,
    responses={200: CategorySerializer(many=True)}
  )
  def get(self, request, format=None):
    tag = request.GET.get('tag', None)
    queries = None
    if tag:
      t = Tag.objects.filter(name=tag).first()
      if t:
        cts = t.ct_tags.all()
        cat_ids = list(cts.values_list('category_id', flat=True))
        queries = Q(id__in=cat_ids)
    resultset = FilterPagination.get_paniation_data(
      request,
      Category,
      CategorySerializer,
      queries=queries,
      order_by_array=None
    )
    return Response(resultset)


class CategoryDetail(APIView):
  permission_classes = []

  def get_object(self, pk):
    try:
      return Category.objects.get(pk=pk)
    except Category.DoesNotExist:
      raise Http404

  @swagger_auto_schema(
    responses={200: CategorySerializer(many=False)}
  )
  def get(self, request, pk, format=None):
    item = self.get_object(pk)
    item.views = item.views + 1
    item.save()
    item = self.get_object(pk)
    serializer = CategorySerializer(item)
    return Response(serializer.data, status=status.HTTP_200_OK)

  @swagger_auto_schema(
    request_body=CategorySerializer(many=False),
    responses={200: CategorySerializer(many=False)}
  )
  def put(self, request, pk, format=None):
    tags = request.data.get('tags', [])
    item = self.get_object(pk)
    serializer = CategorySerializer(item, data=request.data)
    if serializer.is_valid():
      serializer.save()
      # Delete all tags
      item.ct_categories.all().delete()
      # Save category_tags
      for tag_name in tags:
        tag = Tag.objects.filter(name=tag_name).first()
        uct = CategoryTag.objects.update_or_create(category=item, tag=tag)
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    item = self.get_object(pk)
    item.delete()
    return Response(status=status.HTTP_200_OK)


class CategoryCreate(APIView):
  permission_classes = []

  @swagger_auto_schema(
      request_body=NewCategorySerializer(many=False),
      responses={200: CategorySerializer(many=False)}
  )
  def post(self, request, format=None):
    tags = request.data.get('tags', [])

    serializer = NewCategorySerializer(data=request.data, many=False)
    if serializer.is_valid():
      # Create new member with serializer
      new_item = Category.objects.create(**serializer.validated_data)
      new_serializer = CategorySerializer(new_item, many=False)
      # Create category_tags
      for tag_name in tags:
        tag = Tag.objects.filter(name=tag_name).first()
        uct = CategoryTag.objects.update_or_create(category=new_item, tag=tag)
      return Response(new_serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CategoryScanFromFile(APIView):
  permission_classes = []

  @swagger_auto_schema(
      request_body=CategoryScanFromFileSerializer(many=False),
      responses={200: CategorySerializer(many=False)}
  )
  def post(self, request, format=None):
    serializer = CategoryScanFromFileSerializer(data=request.data, many=False)
    if serializer.is_valid():
      # Download and parse the file.
      # Get each eth names
      eth_name = 'test.eth'
      res = scan_ens(eth_name)
      return Response(data=res, status=status.HTTP_201_CREATED)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CategoryNewest(APIView):
  permission_classes = []

  @swagger_auto_schema(
    manual_parameters=FilterPagination.generate_pagination_params(),
    responses={200: CategorySerializer(many=True)}
  )
  def get(self, request, format=None):
    resultset = FilterPagination.get_paniation_data(
      request,
      Category,
      CategorySerializer,
      queries=None,
      order_by_array=None
    )
    return Response(resultset)

class CategoryMostViewd(APIView):
  permission_classes = []

  @swagger_auto_schema(
    manual_parameters=FilterPagination.generate_pagination_params(),
    responses={200: CategorySerializer(many=True)}
  )
  def get(self, request, format=None):
    resultset = FilterPagination.get_paniation_data(
      request,
      Category,
      CategorySerializer,
      queries=None,
      order_by_array=None
    )
    return Response(resultset)

class CategoryMostPurchased(APIView):
  permission_classes = []

  @swagger_auto_schema(
    manual_parameters=FilterPagination.generate_pagination_params(),
    responses={200: CategorySerializer(many=True)}
  )
  def get(self, request, format=None):
    resultset = FilterPagination.get_paniation_data(
      request,
      Category,
      CategorySerializer,
      queries=None,
      order_by_array=None
    )
    return Response(resultset)

class CategoryByTag(APIView):
  permission_classes = []

  @swagger_auto_schema(
    manual_parameters=FilterPagination.generate_pagination_params(),
    responses={200: CategorySerializer(many=True)}
  )
  def get(self, request, format=None):
    resultset = FilterPagination.get_paniation_data(
      request,
      Category,
      CategorySerializer,
      queries=None,
      order_by_array=None
    )
    return Response(resultset)
