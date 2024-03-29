import firebase_admin
from firebase_admin import db, credentials
from firebase_admin import firestore

# authenticate to firebase
cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()