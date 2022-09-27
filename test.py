import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Application Default credentials are automatically created.
print("Starting Credential")
cred = credentials.Certificate('cardcollect-bbefd-a23e50827e56.json')

print("Initialize App")
app = firebase_admin.initialize_app(cred)

print("Connect")
db = firestore.client()

doc_ref = db.collection(u'users').document(u'alovelace')
doc_ref.set({
    u'first': u'Ada',
    u'last': u'Lovelace',
    u'born': 1815
})