""" import firebase_admin
from firebase_admin import credentials, firestore

class ConexaoFirestore:

    def conect(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate("controllers/key-admin.json")
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        return db; """

from firebase_admin import firestore
from controllers.keyAdmin import initialize_firebase  # Explicitly call the function

class ConexaoFirestore:

    def conect(self):
        # Initialize Firebase explicitly
        initialize_firebase()

        # Access Firestore client after Firebase initialization
        db = firestore.client()
        return db
