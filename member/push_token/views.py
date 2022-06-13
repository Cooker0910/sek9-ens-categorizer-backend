import json
import time
from django.utils.timezone import now
from django.shortcuts import render
from django.db import connection, transaction
from django.db import models
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from utils.string_utils import str2bool
from utils.pagination_utils import FilterPagination
from utils.raw_sql_utils import (
  execute_raw_sql_with_pagination,
  execute_raw_sql
)
from .models import PushToken
from .serializers import (
  PushTokenSerializer,
  NewPushTokenSerializer,
)
from authentication.custom_permissions import IsAdminUser
import logging

logger = logging.getLogger(__name__)

class PushTokenList(APIView):
  permission_classes = []

  @swagger_auto_schema(
    manual_parameters=FilterPagination.generate_pagination_params(),
    responses={200: PushTokenSerializer(many=True)}
  )
  def get(self, request, format=None):
    resultset = FilterPagination.get_paniation_data(
      request,
      PushToken,
      PushTokenSerializer,
      queries=None,
      order_by_array=('-id',)
    )
    return Response(resultset)


class PushTokenDetail(APIView):
  def get_object(self, pk):
    try:
      return PushToken.objects.get(pk=pk)
    except PushToken.DoesNotExist:
      raise Http404

  @swagger_auto_schema(
    responses={200: PushTokenSerializer(many=False)}
  )
  def get(self, request, pk, format=None):
    item = self.get_object(pk)
    serializer = PushTokenSerializer(item)
    return Response(serializer.data, status=status.HTTP_200_OK)

  @swagger_auto_schema(
    request_body=PushTokenSerializer(many=False),
    responses={200: PushTokenSerializer(many=False)}
  )
  def put(self, request, pk, format=None):
    item = self.get_object(pk)
    serializer = PushTokenSerializer(item, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    item = self.get_object(pk)
    item.delete()
    return Response(status=status.HTTP_200_OK)


class PushTokenCreate(APIView):
  @swagger_auto_schema(
      request_body=NewPushTokenSerializer(many=False),
      responses={200: PushTokenSerializer(many=False)}
  )
  def post(self, request, member_id , format=None):
    body = request.data
    # Check validation
    member = body['member'] if 'member' in body else None
    plat_form = body['plat_form'] if 'plat_form' in body else None
    udid = body['udid'] if 'udid' in body else None
    player_id = body['player_id'] if 'player_id' in body else None
    push_token = PushToken.objects.filter(member=member_id, plat_form=plat_form).first()
    if push_token:
      push_token.player_id = player_id
      push_token.udid = udid
      push_token.save()
      serializer = PushTokenSerializer(push_token, many=False)
      return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = NewPushTokenSerializer(data=request.data, many=False)
    if serializer.is_valid():
      # Create new member with serializer
      new_item = PushToken.objects.create(**serializer.validated_data)
      new_item.save()
      new_serializer = PushTokenSerializer(new_item, many=False)
      return Response(new_serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
