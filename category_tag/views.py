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
from .models import CategoryTag
from .serializers import (
  CategoryTagSerializer,
  NewCategoryTagSerializer,
)
import logging

logger = logging.getLogger(__name__)

class CategoryTagList(APIView):
  permission_classes = []

  @swagger_auto_schema(
    manual_parameters=FilterPagination.generate_pagination_params(),
    responses={200: CategoryTagSerializer(many=True)}
  )
  def get(self, request, format=None):
    resultset = FilterPagination.get_paniation_data(
      request,
      CategoryTag,
      CategoryTagSerializer,
      queries=None,
      order_by_array=None
    )
    return Response(resultset)


class CategoryTagDetail(APIView):
  permission_classes = []

  def get_object(self, pk):
    try:
      return CategoryTag.objects.get(pk=pk)
    except CategoryTag.DoesNotExist:
      raise Http404

  @swagger_auto_schema(
    responses={200: CategoryTagSerializer(many=False)}
  )
  def get(self, request, pk, format=None):
    item = self.get_object(pk)
    serializer = CategoryTagSerializer(item)
    return Response(serializer.data, status=status.HTTP_200_OK)

  @swagger_auto_schema(
    request_body=CategoryTagSerializer(many=False),
    responses={200: CategoryTagSerializer(many=False)}
  )
  def put(self, request, pk, format=None):
    item = self.get_object(pk)
    serializer = CategoryTagSerializer(item, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    item = self.get_object(pk)
    item.delete()
    return Response(status=status.HTTP_200_OK)


class CategoryTagCreate(APIView):
  permission_classes = []

  @swagger_auto_schema(
      request_body=NewCategoryTagSerializer(many=False),
      responses={200: CategoryTagSerializer(many=False)}
  )
  def post(self, request, format=None):
    serializer = NewCategoryTagSerializer(data=request.data, many=False)
    if serializer.is_valid():
      new_item = CategoryTag.objects.create(**serializer.validated_data)
      new_serializer = CategoryTagSerializer(new_item, many=False)
      return Response(new_serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
