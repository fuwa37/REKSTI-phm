import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import flask

# Use a service account
cred = credentials.Certificate('kunci.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

users_ref = db.collection(u'Pasien')
docs = users_ref.get()

for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))