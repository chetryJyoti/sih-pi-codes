import RPi.GPIO as GPIO 
from time import sleep 

# firebase modules
import os
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from firebase_admin import firestore


GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)
Ena1,In1,In2 = 2,3,4
Ena2,In3,In4 = 14,15,18
GPIO.setup(Ena1,GPIO.OUT)
GPIO.setup(Ena2,GPIO.OUT)
GPIO.setup(In1,GPIO.OUT)
GPIO.setup(In2,GPIO.OUT)
GPIO.setup(In3,GPIO.OUT)
GPIO.setup(In4,GPIO.OUT)
# initialize firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


pwm1 = GPIO.PWM(Ena1,100)
pwm1.start(0)
pwm2 = GPIO.PWM(Ena2,100)
pwm2.start(0)


# while True:
#     print('looping')
#     GPIO.output(In1,GPIO.LOW)
#     GPIO.output(In2,GPIO.HIGH)
#     pwm1.ChangeDutyCycle(100)



while True:
    # readLeftMotorStatus= db.collection('PropellerMotor').document('LeftMotor').get()
    # readRightMotorStatus= db.collection('PropellerMotor').document('RightMotor').get()
    # docDict1 = readLeftMotorStatus.to_dict()
    # docDict2 = readRightMotorStatus.to_dict()
    # leftStatus = docDict1['leftMotorStatus']
    # rightStatus = docDict2['rightMotorStatus']
    # print(leftStatus)
    # print(rightStatus)
    if(leftStatus and rightStatus):
        print('both running')
        GPIO.output(In1,GPIO.LOW)
        GPIO.output(In3,GPIO.LOW)
        GPIO.output(In2,GPIO.HIGH)
        GPIO.output(In4,GPIO.HIGH)
    
    elif(leftStatus):
            print("leftmotoroutput:")
            GPIO.output(In1,GPIO.LOW)
            GPIO.output(In2,GPIO.HIGH)
            # pwm1.ChangeDutyCycle(50)
            # pwm1.ChangeDutyCycle(0)
            # sleep(3)
            # GPIO.output(In1,GPIO.HIGH)
            # GPIO.output(In2,GPIO.LOW)
            # pwm1.ChangeDutyCycle(0)
            # sleep(3)

    elif(rightStatus):
            print("rightmotoroutput:")
            GPIO.output(In3,GPIO.LOW)
            GPIO.output(In4,GPIO.HIGH)
            # pwm2.ChangeDutyCycle(50)
    else:
        GPIO.output(In1,GPIO.LOW)
        GPIO.output(In2,GPIO.LOW)
        GPIO.output(In3,GPIO.LOW)
        GPIO.output(In4,GPIO.LOW)
       



