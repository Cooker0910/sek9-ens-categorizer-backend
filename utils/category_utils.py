from utils.ens_utils import scan_ens
from utils.firebase_utils import (
  auth,
  database,
)
from urllib import request
import csv
import os
import time

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

def add_or_update_eth(category, value):
  print('==== category: ', category)
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
    print('==== e_value: ', e_value)
    # Update
    value['objectId'] = res['objectId']
    database.child('domains').child('eth').child(e_key).child(res['objectId']).update(value)
    return 'updated'
  # Add new category and new eth
  new_value = database.child('domains').child('eth').child(category).push(value)
  # Set objectId
  objectId = new_value['name']
  value['objectId'] = objectId
  database.child('domains').child('eth').child(category).child(objectId).update(value)
  return 'added'


def get_names_from_remote_file(category, file_url):
  response = request.urlretrieve(file_url, "tmp.csv")
  with open('tmp.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
      ens_name = row[0].lower().replace(' ', '-').replace('(', '').replace(')', '')
      value = scan_ens(ens_name)
      print('==== ens: ', ens_name, value)
      # Save into firebase
      add_or_update_eth(category, value)
      time.sleep(2)
  os.remove('tmp.csv')


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
    if cat_files is None:
      continue
    for cf in cat_files:
      print('=== cf: ', cf)
      if ('url' in cf) and cf['url']:
        file_url = cf['url']
        print('=== file_url: ', file_url)
        get_names_from_remote_file(cat_name, file_url)
