# testing snapshot


# firebase modules
import os
from time import sleep
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from firebase_admin import firestore
import threading
# firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# creating an event for notifing main thread
callback_done = threading.Event()

boolValue = False
num1=0

# capturing changes in the database
def on_snapshot(doc_snap,changes,read_time):
    for doc in doc_snap:
        docDict = doc.to_dict()
        # isTrue = docDict['isTrue']
        numValue = docDict['num']
        # print(f'Received document snapshot:{doc.id},isTrue={isTrue}')

        # global boolValue
        # boolValue = isTrue
        global num1
        num1=numValue
    callback_done.set()

doc_ref = db.collection('testC').document('testD')

# watch the document

doc_watch = doc_ref.on_snapshot(on_snapshot)

while True:
    # print(boolValue)
    print(num1)
    sleep(0.5)