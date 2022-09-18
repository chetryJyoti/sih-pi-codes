

import os
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from firebase_admin import firestore

from gpiozero import LED
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

led1 = LED(20)

db = firestore.client()

# creating a collection and document in firebase store
# db.collection("OutputDevice").document("digitalLED").set(
#     {
#         'status':False
#     }
# )



while True:
    readLedStatus= db.collection('OutputDevice').document('digitalLED').get()
    # print(readLedStatus)
    docDict = readLedStatus.to_dict()
    leadStatus = docDict['status']
    print(leadStatus)
    if(leadStatus):
        led1.on()
    else:
        led1.off()



