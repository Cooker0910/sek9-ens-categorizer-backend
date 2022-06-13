import random
import string
import secrets
from member.models import Member

def get_member_model():
  return Member

def get_lab():
  return Member.objects.filter(type=Member.LAB).order_by('id').first()

def get_admin():
  return Member.objects.filter(type=Member.ADMIN).order_by('id').first()


def generate_password():
  symbols = string.punctuation
  password = ""
  for _ in range(9):
    password += secrets.choice(string.ascii_lowercase)
  password += secrets.choice(string.ascii_uppercase)
  password += secrets.choice(string.digits)
  password += secrets.choice(symbols)
  return password
