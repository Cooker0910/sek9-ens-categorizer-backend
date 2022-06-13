from rest_framework import serializers
from member.models import Member
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizes JWT default Serializer to add more information about user"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.name
        token['email'] = user.email
        token['is_superuser'] = user.is_superuser
        token['is_staff'] = user.is_staff
        return token

class LoginSerializer(serializers.ModelSerializer):
  class Meta:
    model = Member
    fields = (
      'email',
      'password',
    )


class RegisterSerializer(serializers.ModelSerializer):
  class Meta:
    model = Member
    fields = (
      'email',
      'type',
      'first_name',
      'last_name',
      'sex',
      'telnumber',
      'birth_date',
      'password',
      'plat_form',
      'udid',
    )


class RegisterByEmailSerializer(serializers.ModelSerializer):
  class Meta:
    model = Member
    fields = (
      'email',
      'type',
      'first_name',
      'last_name',
      'sex',
      'telnumber',
      'birth_date',
      'password',
      'plat_form',
      'udid',
    )

class ChangeEmailSerializer(serializers.ModelSerializer):
  class Meta:
    model = Member
    fields = (
      'email',
      'new_email'
    )

class ChangePasswordSerializer(serializers.ModelSerializer):
  class Meta:
    model = Member
    fields = (
      'email',
      'new_password'
    )

class ForgetPasswordSerializer(serializers.ModelSerializer):
  class Meta:
    model = Member
    fields = (
      'email',
    )
