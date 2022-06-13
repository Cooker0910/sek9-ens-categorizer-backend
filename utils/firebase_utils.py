from django.shortcuts import render
import pyrebase

config={
  "apiKey": "AIzaSyC_6jTjTjO-C_59Hoo_nViXRZkhpyHxmnw",
  "databaseURL": 'https://sek9-a1d71-default-rtdb.firebaseio.com',
  "authDomain": "sek9-a1d71.firebaseapp.com",
  "projectId": "sek9-a1d71",
  "storageBucket": "sek9-a1d71.appspot.com",
  "messagingSenderId": "330243897942",
  "appId": "1:330243897942:web:d874c23bba865109bed9f7",
  "measurementId": "G-CFZRT4XVLR"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
storage = firebase.storage()
database=firebase.database()
FIREBASE_AUTH_EMAIL = 'admin@email.com'
FIREBASE_AUTH_PASSWORD = '123qweasd'
