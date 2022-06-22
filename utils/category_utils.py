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
    for row in reader:
      value = None
      ens_name = row[0].lower().replace(' ', '').replace('(', '').replace(')', '').replace("'", '')
      for domain in domains:
        value = scan_ens(f"{ens_name}.{domain.name}")
        print('==== ens: ', ens_name, value)
        # Save into firebase
        add_or_update_eth(category, domain, ens_name, value)
        time.sleep(1)
      time.sleep(2)
  os.remove('tmp.csv')


def get_category_by_name(category_name):
  return Category.objects.filter(name=category_name).first()


def scan_category(category_name):
  # Get categories from Firebase
  category = Category.objects.filter(name=category_name).first()
  if category is None:
    print(f"==== The category {category_name} don't exist")
    return
  cat_files = category.files
  if cat_files is None:
    return
  for cf in cat_files:
    print('=== cf: ', cf)
    if ('url' in cf) and cf['url']:
      file_url = cf['url']
      print('=== file_url: ', file_url)
      get_names_from_remote_file(category, file_url)
    time.sleep(1)  
  time.sleep(1)

def scan_categories():
  categories = Category.objects.all()
  for cat in categories:
    cat_files = cat.files
    print('\n==== Checking category: ', cat.name)
    if cat_files is None:
      continue
    for cf in cat_files:
      print('=== cf: ', cf)
      if ('url' in cf) and cf['url']:
        file_url = cf['url']
        print('=== file_url: ', file_url)
        get_names_from_remote_file(cat, file_url)
    # Calculate summary
    eths = cat.category_ethereums.all()
    cat.floor = eths.aggregate(Sum('balance'))['balance__sum']
    cat.save()



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
    common_scan_category_by_re(cat, regExpress, user_token=None, limit=None)
    time.sleep(1)
