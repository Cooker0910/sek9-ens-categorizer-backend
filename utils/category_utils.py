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
from utils import exrex

def is_existing_value(cat_name, eth_name):
  try:
    print('=== is_existing_value: ', cat_name, eth_name)
    eths = database.child('domains').child('eth').child(cat_name).get()
    for e in eths.each():
      e_key = e.key()
      e_value = e.val()
      if ('name' in e_value) and (e_value['name'] == eth_name):
        return {'objectId': e_key, 'name': e_value['name']}
  except Exception as error:
    print('==== error: ', error)
  return None

def add_or_update_eth(category, value, user_token=None):
  try:
    eths = database.child('domains').child('eth').get()
    for e in eths.each():
      e_key = e.key()
      e_value = e.val()
      print('==== e_key: ', e_key)
      if e_key != category:
        continue
      # Check existing
      res = is_existing_value(category, value['name'])
      if res is None:
        break
      print('==== res: ', res)

      # Update
      value['objectId'] = res['objectId']
      database.child('domains').child('eth').child(e_key).child(res['objectId']).update(value, user_token)
      return 'updated'
    # Add new category and new eth
    new_value = database.child('domains').child('eth').child(category).push(value, user_token)
    # Set objectId
    objectId = new_value['name']
    value['objectId'] = objectId
    database.child('domains').child('eth').child(category).child(objectId).update(value)
    return 'added'
  except Exception as error:
    print('==== Failed to add/update eth: add_or_update_eth(): ', error)
  return 'failed'


def get_names_from_remote_file(category, file_url, user_token=None):
  response = request.urlretrieve(file_url, "tmp.csv")
  with open('tmp.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
      value = None
      ens_name = row[0].lower().replace(' ', '-').replace('(', '').replace(')', '')
      value = scan_ens(ens_name)
      print('==== ens: ', ens_name, value)
      # Save into firebase
      add_or_update_eth(category, value, user_token=user_token)
      time.sleep(2)
  os.remove('tmp.csv')

def get_category_by_name(category_name):
  # Get categories from Firebase
  categories = database.child('categories').get()
  res = None
  for cat in categories.each():
    cat_key = cat.key()
    cat_value = cat.val()
    cat_name = cat_value['name']
    if category_name != cat_name:
      continue
    res = cat_value
  return res

def scan_category(category):
  # Get categories from Firebase
  categories = database.child('categories').get()
  for cat in categories.each():
    cat_key = cat.key()
    cat_value = cat.val()
    cat_name = cat_value['name']
    if category != cat_name:
      continue
    cat_files = cat_value['files'] if 'files' in cat_value else None
    if cat_files is None:
      continue
    for cf in cat_files:
      print('=== cf: ', cf)
      if ('url' in cf) and cf['url']:
        file_url = cf['url']
        print('=== file_url: ', file_url)
        get_names_from_remote_file(category, file_url)
      time.sleep(1)  
    time.sleep(1)

def scan_categories():
  # Get categories from Firebase
  categories = database.child('categories').get()
  for cat in categories.each():
    cat_key = cat.key()
    cat_value = cat.val()
    cat_name = cat_value['name']
    cat_files = cat_value['files'] if 'files' in cat_value else None
    print('\n==== Checking category: ', cat_name)
    if cat_files is None:
      continue
    for cf in cat_files:
      print('=== cf: ', cf)
      if ('url' in cf) and cf['url']:
        file_url = cf['url']
        print('=== file_url: ', file_url)
        get_names_from_remote_file(cat_name, file_url)


def common_scan_category_by_re(category_name, reg_express, user_token=None, limit=None):
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
    value = scan_ens(ens_name, skip_no_eth=True)
    print('==== ens: ', ens_name, value)
    # Save into firebase
    if value is not None:
      add_or_update_eth(category_name, value, user_token=user_token)
    time.sleep(2)
  return None

def scan_category_by_re(category, limit=None):
  # Get category from Firebase
  cat = get_category_by_name(category)
  regExpress = cat['regularExpression']
  print('==== regExpress: ', regExpress)
  common_scan_category_by_re(category, regExpress, limit=None)
  

def scan_categories_by_re(limit=None):
  firebase_user = auth.sign_in_with_email_and_password(FIREBASE_AUTH_EMAIL, FIREBASE_AUTH_PASSWORD)
  # Get categories from Firebase
  categories = database.child('categories').get()
  for cat in categories.each():
    cat_key = cat.key()
    cat_value = cat.val()
    cat_name = cat_value['name']
    print('\n==== Checking category: ', cat_name)
    if 'regularExpression' in cat:
      regExpress = cat['regularExpression']
      print('==== regExpress: ', regExpress)
      common_scan_category_by_re(cat_name, regExpress, user_token=firebase_user['idToken'], limit=None)
    time.sleep(1)
