import json
import requests
from datetime import datetime
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from config import settings
from member.models import Member
from member.serializers import MemberSerializer

from .serializers import (
  LoginSerializer,
  RegisterSerializer,
  RegisterByEmailSerializer,
  ForgetPasswordSerializer,
  ChangeEmailSerializer,
  ChangePasswordSerializer,
  CustomTokenObtainPairSerializer
)
from .custom_admin_jwt import (
  custom_admin_authentication,
  admin_jwt_payload_handler,
  admin_jwt_encode_handler
)
from .custom_jwt import (
  jwt_payload_handler,
  jwt_encode_handler
)
from email_verification import send_email, send_email_password_reset, send_email_reset, send_password_reset
import logging
# from users import serializers
from rest_framework_simplejwt.views import TokenObtainPairView

logger = logging.getLogger(__name__)

class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer

class CustomLogin(APIView):
    permission_classes = []

    def process_admin_user(self, request, admin, serializer):
      admin_user = custom_admin_authentication(
        request, 
        email=serializer.data['email'],
        password=serializer.data['password']
      )
      if admin_user is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
      else:
        payload = admin_jwt_payload_handler(admin_user)
        # Generate admin jwt token
        token = admin_jwt_encode_handler(payload)
        return Response({'token': token, 'member': payload})

    def process_member(self, request, member, serializer):
      if (member.password != serializer.data['password']) and (not serializer.data['email'] is None):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
      member.login_date = datetime.now()
      member.save()
      payload = jwt_payload_handler(member)
      token = jwt_encode_handler(payload)
      return Response({'token': token, 'member': payload})

    @swagger_auto_schema(
        request_body=LoginSerializer(many=False),
        responses={200: MemberSerializer(many=False)}
    )
    def post(self, request, format=None):
      serializer = LoginSerializer(
        data=request.data,
        context={'request': request}
      )
      serializer.is_valid(raise_exception=True)
      member = None
      if ('email' in serializer.data) and (not serializer.data['email'] is None):
        # Check members for general user.
        member = Member.objects.filter(email__iexact=serializer.data['email']).first()
      if member is None:
        # Check admin user.
        admin = User.objects.filter(email__iexact=serializer.data['email']).first()
        if admin is None:
          return Response(status=status.HTTP_404_NOT_FOUND)
        return self.process_admin_user(request, admin, serializer)

      # Generate member jwt token
      return self.process_member(request, member, serializer)


class CustomLoginByEmail(APIView):
    permission_classes = []

    def process_admin_user(self, request, admin, serializer):
      admin_user = custom_admin_authentication(
        request, 
        email=serializer.data['email'],
        password=serializer.data['password']
      )
      if admin_user is None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
      else:
        payload = admin_jwt_payload_handler(admin_user)
        # Generate admin jwt token
        token = admin_jwt_encode_handler(payload)
        return Response({'token': token, 'member': payload})

    def process_member(self, request, member, serializer):
      if member.password != serializer.data['password']:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
      member.login_date = datetime.now()
      member.save()
      payload = jwt_payload_handler(member)
      token = jwt_encode_handler(payload)
      return Response({'token': token, 'member': payload})

    @swagger_auto_schema(
        request_body=LoginSerializer(many=False),
        responses={200: MemberSerializer(many=False)}
    )
    def post(self, request, format=None):
      serializer = LoginSerializer(
        data=request.data,
        context={'request': request}
      )
      serializer.is_valid(raise_exception=True)
      email = serializer.data['email'] if ('email' in serializer.data) else None
      udid = serializer.data['udid'] if ('udid' in serializer.data) else None
      member = Member.objects.filter(email=serializer.data['email']).first()
      if member is None:
        # Check admin user.
        admin = User.objects.filter(email=serializer.data['email']).first()
        if admin is None:
          return Response(status=status.HTTP_404_NOT_FOUND)
        return self.process_admin_user(request, admin, serializer)

      # Generate member jwt token
      return self.process_member(request, member, serializer)


class Logout(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        # simply delete the token to force a login
        user = request.user
        try:
            user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            logger.error('logout error.')
            pass
        
        return Response({}, status=status.HTTP_200_OK)


class Register(APIView):
    permission_classes = []

    @swagger_auto_schema(
        request_body=RegisterSerializer(many=False),
        responses={200: MemberSerializer(many=False)}
    )
    def post(self, request, format=None):      
      serializer = RegisterSerializer(data=request.data, many=False)
      if serializer.is_valid():
        # if 'udid' in serializer.data:
        #   item = Member.objects.filter(udid=serializer.data['udid']).first()
        #   item_serializer = MemberSerializer(item, many=False)
        #   if item:
        #     return Response(item_serializer.data, status=status.HTTP_201_CREATED)
        new_item = Member(**serializer.validated_data)
        new_item.save()
        new_serializer = MemberSerializer(new_item, many=False)
        return Response(new_serializer.data, status=status.HTTP_201_CREATED)
      return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ChangeUserInfo(APIView):
  permission_classes = []

  @swagger_auto_schema(
      request_body=RegisterSerializer(many=False),
      responses={200: MemberSerializer(many=False)}
  )

  def post(self, request, format=None):      
    serializer = LoginSerializer(
      data=request.data,
      context={'request': request}
    )
    serializer.is_valid(raise_exception=True)

    is_member = None
    if ('email' in serializer.data) and (not serializer.data['email'] is None):  
      print(76, 'email', serializer.data)
      # Check members for general user.
      is_member = Member.objects.filter(email=serializer.data['email']).first()

    if is_member is None:
      # Check admin user.
      member = Member.objects.filter(udid=serializer.data['udid']).first()
      if member is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
      else:
        member.email = serializer.data['email']
        member.password = serializer.data['password']
        member.save()
        payload = jwt_payload_handler(member)
        token = jwt_encode_handler(payload)
        return Response({'token': token, 'member': payload})

    return Response(status=status.HTTP_404_NOT_FOUND)


class RegisterByEmail(APIView):
    permission_classes = []
    
    def update_and_resend_verifiction_token(self, request, member):
      member_serializer = MemberSerializer(member, request.data)
      if member_serializer.is_valid():
        member_serializer.save()
        member.save()
        send_email(member)
        return Response(member_serializer.validated_data, status=status.HTTP_200_OK)
      else:
        return Response({'error': member_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=RegisterByEmailSerializer(many=False),
        responses={200: MemberSerializer(many=False)}
    )
    def post(self, request, format=None):      
      serializer = RegisterByEmailSerializer(data=request.data, many=False)
      if serializer.is_valid():
        # Check validation
        email = serializer.data['email'] if 'email' in serializer.data else None
        udid = serializer.data['udid'] if 'udid' in serializer.data else None
        if email is None:
          return Response({'email': ['Missed email field',]}, status=status.HTTP_400_BAD_REQUEST)
        if udid is None:
          return Response({'udid': ['Missed udid field.',]}, status=status.HTTP_400_BAD_REQUEST)
        
        member = Member.objects.filter(email=email).first()
        if member:
          if member.confirmed:
            # If member already registered and confirmed, skip.
            return Response({'error': 'Member with this email address already exists.'}, status=status.HTTP_400_BAD_REQUEST)
          else:
            # If member already was registered and not confirmed,
            # update with body and send verification token via email.
            return self.update_and_resend_verifiction_token(request, member)
        else:
          # If member not exist, check udid.)
          member = Member.objects.filter(udid=udid).first()
          if member is None:
            # create new member record and send verification token via email
            new_member = Member(**serializer.validated_data)
            new_member.save()
            # send_email(new_member)
            new_serializer = MemberSerializer(new_member, many=False)
            return Response(new_serializer.data, status=status.HTTP_201_CREATED)

          if member.confirmed:
            return Response({'error': 'Member with this email address already exists.'}, status=status.HTTP_400_BAD_REQUEST)
          else:
            return self.update_and_resend_verifiction_token(request, member)

      return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ForgetPassword(APIView):
    permission_classes = []

    @swagger_auto_schema(
        request_body=ForgetPasswordSerializer(many=False),
        responses={200: {}}
    )
    def post(self, request, format=None):      
      serializer = ForgetPasswordSerializer(data=request.data, many=False)
      if serializer.is_valid():
        # Check validation
        email = serializer.data['email'] if 'email' in serializer.data else None
        if email is None:
          return Response({'email': ['Missed email field',]}, status=status.HTTP_400_BAD_REQUEST)
        
        member = Member.objects.filter(email=email).first()
        if member:
          # if member.confirmed:
          send_email_password_reset(member)
          return Response({'result': 'A reset password email has been sent to ' + email + '.'}, status=status.HTTP_200_OK)
          # else:
          #   return Response({'error': 'Member with this email address was not verifyed yet.'}, status=status.HTTP_400_BAD_REQUEST)

        else:
          return Response({'error': 'Member with this email address don\'t exist.'}, status=status.HTTP_404_NOT_FOUND)

      return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ChangeUserInfoMail(APIView):
    permission_classes = []

    @swagger_auto_schema(
        request_body=ChangeEmailSerializer(many=False),
        responses={200: {}}
    )
    def post(self, request, format=None):      
      serializer = ChangeEmailSerializer(data=request.data, many=False)
      if serializer.is_valid():
        # Check validation
        email = serializer.data['email'] if 'email' in serializer.data else None
        if email is None:
          return Response({'email': ['Missed email field',]}, status=status.HTTP_400_BAD_REQUEST)
        
        member = Member.objects.filter(email=email).first()
        if member:
          if member.confirmed:
            send_email_reset(member, serializer.data['new_email'])
            return Response({'result': 'A reset password email has been sent to ' + email + '.'}, status=status.HTTP_200_OK)
          else:
            return Response({'error': 'Member with this email address was not verifyed yet.'}, status=status.HTTP_400_BAD_REQUEST)

        else:
          return Response({'error': 'Member with this email address don\'t exist.'}, status=status.HTTP_404_NOT_FOUND)

      return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ChangeUserInfoPassword(APIView):
    permission_classes = []

    @swagger_auto_schema(
        request_body=ChangePasswordSerializer(many=False),
        responses={200: {}}
    )
    def post(self, request, format=None):      
      serializer = ChangePasswordSerializer(data=request.data, many=False)
      if serializer.is_valid():
        # Check validation
        email = serializer.data['email'] if 'email' in serializer.data else None
        if email is None:
          return Response({'email': ['Missed email field',]}, status=status.HTTP_400_BAD_REQUEST)
        
        member = Member.objects.filter(email=email).first()
        if member:
          if member.confirmed:
            send_password_reset(member, serializer.data['new_password'])
            return Response({'result': 'A reset password email has been sent to ' + email + '.'}, status=status.HTTP_200_OK)
          else:
            return Response({'error': 'Member with this email address was not verifyed yet.'}, status=status.HTTP_400_BAD_REQUEST)

        else:
          return Response({'error': 'Member with this email address don\'t exist.'}, status=status.HTTP_404_NOT_FOUND)

      return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)