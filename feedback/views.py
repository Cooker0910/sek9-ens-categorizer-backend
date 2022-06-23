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
from utils.string_utils import str2bool
from utils.pagination_utils import (
  FilterPagination,
)
from .models import Feedback
from .serializers import (
  FeedbackSerializer,
  NewFeedbackSerializer,
)
from utils.ens_utils import scan_ens
import logging

logger = logging.getLogger(__name__)

class FeedbackList(APIView):
  permission_classes = []

  @swagger_auto_schema(
    manual_parameters=FilterPagination.generate_pagination_params(),
    responses={200: FeedbackSerializer(many=True)}
  )
  def get(self, request, format=None):
    resultset = FilterPagination.get_paniation_data(
      request,
      Feedback,
      FeedbackSerializer,
      queries=None,
      order_by_array=('name',)
    )
    return Response(resultset)


class FeedbackDetail(APIView):
  permission_classes = []

  def get_object(self, pk):
    try:
      return Feedback.objects.get(pk=pk)
    except Feedback.DoesNotExist:
      raise Http404

  @swagger_auto_schema(
    responses={200: FeedbackSerializer(many=False)}
  )
  def get(self, request, pk, format=None):
    item = self.get_object(pk)
    serializer = FeedbackSerializer(item)
    return Response(serializer.data, status=status.HTTP_200_OK)

  @swagger_auto_schema(
    request_body=FeedbackSerializer(many=False),
    responses={200: FeedbackSerializer(many=False)}
  )
  def put(self, request, pk, format=None):
    item = self.get_object(pk)
    serializer = FeedbackSerializer(item, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, pk, format=None):
    item = self.get_object(pk)
    item.delete()
    return Response(status=status.HTTP_200_OK)


class FeedbackCreate(APIView):
  permission_classes = []

  @swagger_auto_schema(
      request_body=NewFeedbackSerializer(many=False),
      responses={200: FeedbackSerializer(many=False)}
  )
  def post(self, request, format=None):
    serializer = NewFeedbackSerializer(data=request.data, many=False)
    if serializer.is_valid():
      # Create new member with serializer
      new_item = Feedback.objects.create(**serializer.validated_data)
      new_serializer = FeedbackSerializer(new_item, many=False)
      return Response(new_serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
