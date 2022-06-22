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
  get_queryset_from_request
)
from utils.raw_sql_utils import (
  execute_raw_sql_with_pagination,
  execute_raw_sql
)
from utils.member_utils import generate_password, get_lab
from utils.email_utils import send_email_member_password
from .models import Member
from .serializers import (
  MemberSerializer,
  NewMemberSerializer,
)
import logging

logger = logging.getLogger(__name__)

class MemberList(APIView):
  permission_classes = []

  @swagger_auto_schema(
    manual_parameters=FilterPagination.generate_pagination_params(),
    responses={200: MemberSerializer(many=True)}
  )
  def get(self, request, format=None):
    resultset = FilterPagination.get_paniation_data(
      request,
      Member,
      MemberSerializer,
      queries=None,
      order_by_array=('-id',)
    )
    return Response(resultset)


class MemberDetail(APIView):
  def get_object(self, pk):
    try:
      return Member.objects.get(pk=pk)
    except Member.DoesNotExist:
      raise Http404

  @swagger_auto_schema(
    responses={200: MemberSerializer(many=False)}
  )
  def get(self, request, pk, format=None):
    item = self.get_object(pk)
    serializer = MemberSerializer(item)
    return Response(serializer.data, status=status.HTTP_200_OK)

  @swagger_auto_schema(
    request_body=MemberSerializer(many=False),
    responses={200: MemberSerializer(many=False)}
  )
  def put(self, request, pk, format=None):
    item = self.get_object(pk)
    serializer = MemberSerializer(item, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    item = self.get_object(pk)
    item.delete()
    return Response(status=status.HTTP_200_OK)


class MemberCreate(APIView):
  @swagger_auto_schema(
      request_body=NewMemberSerializer(many=False),
      responses={200: MemberSerializer(many=False)}
  )
  def post(self, request, format=None):
    serializer = NewMemberSerializer(data=request.data, many=False)
    if serializer.is_valid():
      # Create new member with serializer
      new_item = Member.objects.create(**serializer.validated_data)
      # Generate password
      new_item.password = generate_password()
      new_item.save()
      # Send email
      send_email_member_password(new_item, True)
      new_serializer = MemberSerializer(new_item, many=False)
      return Response(new_serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

