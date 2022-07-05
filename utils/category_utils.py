from ethereum.views import EthereumScan
from utils.ens_utils import scan_ens
from utils.firebase_utils import (
  auth,
  database,
  FIREBASE_AUTH_EMAIL,
  FIREBASE_AUTH_PASSWORD
)
from urllib import request
import csv
import os
import time
import json
from utils import exrex
from django.db.models import Avg, Count, Min, Sum
from category.models import Category
from domain.models import Domain
from ethereum.models import Ethereum

def is_existing_value(category, domain, eth_name):
  print('=== is_existing_value: ', category.name, eth_name)
  # eths = database.child('domains').child('eth').child(cat_name).get()
  eth = Ethereum.objects.filter(category=category, domain=domain, name=eth_name).first()
  return eth

def repaire_category_balance(category):
  eths = category.category_ethereums.all()
  balance = eths.aggregate(Sum('balance'))['balance__sum']
  owners = eths.aggregate(Sum('owners'))['owners__sum'] #eths.filter(owner__isnull=False, owner__regex = r"\S+").all().count()
  available = eths.filter(address__isnull=False, owner__regex = r"\S+").count()
  count = eths.count()
  category.floor = balance if balance else 0
  category.owners = owners if owners else 0
  category.available = available
  category.count = count
  category.save()
  print(f'==== category={category.name}, balance={category.floor}, owners={category.owners}, available/count={available}/{count}')

def add_or_update_eth(category, domain, ens_name, value, user_token=None):
  try:
    new_values = value
    new_values['data'] = json.dumps(value)
    new_values['name'] = ens_name
    # {
    #   'address': value['address'],
    #   'owner': None,
    #   'description': None,
    #   'created_date': None,
    #   'resolver': value['resolver'],
    #   'registrant': None,
    #   'registration_date': None,
    #   'expiry_date': None,
    #   'starting_price': 0,
    #   'end_price': 0,
    #   'end_date': None,
    #   'label_hash': value['address'],
    #   'payment_token': None,
    #   'last_sale': 0,
    #   'width': 0,
    #   'balance': value['balance'],
    #   'data': json.dumps(value),
    # }
    Ethereum.objects.update_or_create(category=category, domain=domain, name=ens_name, defaults=value)
      
  except Exception as error:
    print('==== Failed to add/update eth: add_or_update_eth(): ', error)
  return 'failed'


def get_names_from_remote_file(category, file_url, user_token=None):
  response = request.urlretrieve(file_url, "tmp.csv")
  domains = Domain.objects.all()
  with open('tmp.csv', 'r') as file:
    reader = csv.reader(file)
    index = 1
    for row in reader:
      value = None
      ens_name = row[0].lower().replace(' ', '').replace('(', '').replace(')', '').replace("'", '')
      for domain in domains:
        print(f'==== category = {category.name}, domain = {domain.name}')
        value = scan_ens(f"{ens_name}.{domain.name}")
        print(f'==== {index}: ens = {ens_name}, value = {value}')
        # Save into firebase
        add_or_update_eth(category, domain, ens_name, value)
        time.sleep(2)
      index = index + 1
      time.sleep(3)
  os.remove('tmp.csv')


def get_category_by_name(category_name):
  return Category.objects.filter(name=category_name).first()


def common_scan_category(category):
  cat_files = category.files
  if cat_files is None:
    return
  print('\n==== Checking category: ', category.name)
  for cf in cat_files:
    print('=== cf: ', cf)
    if ('url' in cf) and cf['url']:
      file_url = cf['url']
      print('=== file_url: ', file_url)
      get_names_from_remote_file(category, file_url)
    time.sleep(1)  
  time.sleep(1)

def scan_category(category_name):
  # Get categories from Firebase
  category = Category.objects.filter(name=category_name).first()
  if category is None:
    print(f"==== The category {category} don't exist")
    return
  common_scan_category(category)

def scan_category_by_id(category_id):
  category = Category.objects.filter(id=category_id).first()
  if category is None:
    print(f"==== The category {category_id} don't exist")
    return
  common_scan_category(category)

def scan_categories():
  categories = Category.objects.all()
  for cat in categories:
    common_scan_category(cat)
    repaire_category_balance(cat)
    time.sleep(3)


def common_scan_category_by_re(category, reg_express, user_token=None, limit=None):
  # Check validation
  if (reg_express is None) or (reg_express == ''):
    return None

  # Generate strings matching to RE
  ens_names = []
  if limit:
    ens_names = list(exrex.generate(reg_express, limit=limit))[:limit]
  else:
    ens_names = list(exrex.generate(reg_express))
  print('==== generated eth names: ', len(ens_names))
  
  # Scan eth names
  for ens_name in ens_names:
    domains = Domain.objects.all()
    for domain in domains:
      value = scan_ens(f"{ens_name}.{domain.name}", skip_no_eth=True)
      print('==== ens: ', ens_name, value)
      # Save into firebase
      if value is not None:
        add_or_update_eth(category, domain, ens_name, value)
      time.sleep(2)
    time.sleep(3)
  return None

def scan_category_by_re(category_name, limit=None):
  # Get category from Firebase
  cat = get_category_by_name(category_name)
  regExpress = cat.regular_expression
  print('==== regExpress: ', regExpress)
  common_scan_category_by_re(cat, regExpress, limit=None)
  

def scan_categories_by_re(limit=None):
  # firebase_user = auth.sign_in_with_email_and_password(FIREBASE_AUTH_EMAIL, FIREBASE_AUTH_PASSWORD)
  # Get categories from Firebase
  categories = Category.objects.all()
  for cat in categories:
    cat_name = cat.name
    print('\n==== Checking category: ', cat_name)
    regExpress = cat.regular_expression
    print('==== regExpress: ', regExpress)
    common_scan_category_by_re(cat, regExpress, user_token=None, limit=1000)
    time.sleep(5)
