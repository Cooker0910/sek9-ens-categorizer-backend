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
from .models import Favorit
from .serializers import (
  FavoritSerializer,
  NewFavoritSerializer,
)
from member.models import Member
import logging

logger = logging.getLogger(__name__)

class FavoritList(APIView):
  permission_classes = []
  user_param = openapi.Parameter(
    'user_id',
    openapi.IN_QUERY,
    description='User ID.',
    type=openapi.TYPE_STRING
  )
  paramenters = [user_param,] + FilterPagination.generate_pagination_params()

  @swagger_auto_schema(
    manual_parameters=paramenters,
    responses={200: FavoritSerializer(many=True)}
  )
  def get(self, request, format=None):
    user_id = request.GET.get('user_id', None)
    queries = None
    if user_id:
      queries = Q(member_id=user_id)
    resultset = FilterPagination.get_paniation_data(
      request,
      Favorit,
      FavoritSerializer,
      queries=queries,
      order_by_array=('member', 'ethereum')
    )
    return Response(resultset)


class FavoritListByCategoryId(APIView):
  permission_classes = []

  @swagger_auto_schema(
    manual_parameters=FilterPagination.generate_pagination_params(),
    responses={200: FavoritSerializer(many=True)}
  )
  def get(self, request, format=None):
    resultset = FilterPagination.get_paniation_data(
      request,
      Favorit,
      FavoritSerializer,
      queries=None,
      order_by_array=('name',)
    )
    return Response(resultset)


class FavoritDetail(APIView):
  permission_classes = []

  def get_object(self, pk):
    try:
      return Favorit.objects.get(pk=pk)
    except Favorit.DoesNotExist:
      raise Http404

  @swagger_auto_schema(
    responses={200: FavoritSerializer(many=False)}
  )
  def get(self, request, pk, format=None):
    item = self.get_object(pk)
    serializer = FavoritSerializer(item)
    return Response(serializer.data, status=status.HTTP_200_OK)

  @swagger_auto_schema(
    request_body=FavoritSerializer(many=False),
    responses={200: FavoritSerializer(many=False)}
  )
  def put(self, request, pk, format=None):
    item = self.get_object(pk)
    serializer = FavoritSerializer(item, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    item = self.get_object(pk)
    item.delete()
    return Response(status=status.HTTP_200_OK)


class FavoritCreate(APIView):
  permission_classes = []

  @swagger_auto_schema(
      request_body=NewFavoritSerializer(many=False),
      responses={200: FavoritSerializer(many=False)}
  )
  def post(self, request, format=None):
    serializer = NewFavoritSerializer(data=request.data, many=False)
    if serializer.is_valid():
      # Create new member with serializer
      new_item = Favorit.objects.create(**serializer.validated_data)
      new_serializer = FavoritSerializer(new_item, many=False)
      return Response(new_serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
