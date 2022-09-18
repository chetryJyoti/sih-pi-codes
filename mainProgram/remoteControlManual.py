# object oriented MAIN CODE

import RPi.GPIO as GPIO          
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# firebase modules
import os
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from firebase_admin import firestore
import threading

# firebase intialize
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# creating an event for notifing main thread
callback_done = threading.Event()


# leftStatus=False
# rightStatus=False

# capturing changes in the database


# def on_snapshot(doc_snap,changes,read_time):
#     print(doc_snap)
#     for doc in doc_snap:
#         docDict = doc.to_dict()
#         print(docDict['leftmotor'])
#         if(docDict['leftmotor']=="Lmotor"):
#             print(docDict)
#             leftMotorStatus=docDict['leftMotorStatus']
#             global leftStatus
#             leftStatus=leftMotorStatus
#         elif(docDict['rightMotor']=="Rmotor"):
#             RightMotorStatus=docDict['rightMotorStatus']
#             global rightStatus
#             rightStatus=RightMotorStatus
#     callback_done.set()


# doc_ref_LeftMotor = db.collection('PropellerMotor').document('LeftMotor')
# doc_ref_RightMotor = db.collection('PropellerMotor').document('RightMotor')

# # watch the document
# doc_watch1 = doc_ref_LeftMotor.on_snapshot(on_snapshot)
# doc_watch2 = doc_ref_RightMotor.on_snapshot(on_snapshot)

# 
class Motor():
    def __init__(self,Ena,In1,In2):
        self.Ena = Ena
        self.In1= In1
        self.In2 = In2

        GPIO.setup(self.Ena,GPIO.OUT)
        GPIO.setup(self.In1,GPIO.OUT)
        GPIO.setup(self.In2,GPIO.OUT)
        self.pwm = GPIO.PWM(self.Ena,100)
        self.pwm.start(0)
    

    # def moveForwardSpeed(self,x=50,t=0):
    #     GPIO.output(self.In1,GPIO.LOW)
    #     GPIO.output(self.In2,GPIO.HIGH)
    #     self.pwm.ChangeDutyCycle(x)
        # sleep(t)

    # def moveBackward(self,x=50,t=0):
    #     GPIO.output(self.In1,GPIO.HIGH)
    #     GPIO.output(self.In2,GPIO.LOW)
    #     self.pwm.ChangeDutyCycle(x)
    #     sleep(t)

    # left motor control
    def LeftSide(self,leftMotorSpeed):
         GPIO.output(self.In1,GPIO.LOW)
         GPIO.output(self.In2,GPIO.HIGH)
         self.pwm.ChangeDutyCycle(leftMotorSpeed)

    def leftSideReverse(self,leftMotorSpeed):
         GPIO.output(self.In1,GPIO.HIGH)
         GPIO.output(self.In2,GPIO.LOW)
         self.pwm.ChangeDutyCycle(leftMotorSpeed)
    

    # right motor control

    def RightSide(self,rightMotorSpeed):
         GPIO.output(self.In1,GPIO.LOW)
         GPIO.output(self.In2,GPIO.HIGH)
         self.pwm.ChangeDutyCycle(rightMotorSpeed)

    def rightSideReverse(self,rightMotorSpeed):
         GPIO.output(self.In1,GPIO.HIGH)
         GPIO.output(self.In2,GPIO.LOW)
         self.pwm.ChangeDutyCycle(rightMotorSpeed)

    def sameSpeed(self,constSpeed=60):
        self.RightSide(constSpeed)
        self.LeftSide(constSpeed)

    def stopMotor(self):
        GPIO.output(self.In1,GPIO.LOW)
        GPIO.output(self.In2,GPIO.LOW)
        self.pwm.ChangeDutyCycle(0)

   
    
        
# Ena in1 in2
motor1 = Motor(2,3,4)
# Enb in3 in4
motor2 =Motor(14,15,18)


while True:
    readLeftMotorStatus= db.collection('PropellerMotor').document('LeftMotor').get()
    readRightMotorStatus= db.collection('PropellerMotor').document('RightMotor').get()

    docDict1 = readLeftMotorStatus.to_dict()
    docDict2 = readRightMotorStatus.to_dict()
    leftStatus = docDict1['leftMotorStatus']
    leftMotorSpeed=docDict1['leftMotorSpeed']
    leftMotorReverse=docDict1['leftMotorReverse']

    rightStatus = docDict2['rightMotorStatus']
    rightMotorSpeed =docDict2['rightMotorSpeed']
    rightMotorReverse=docDict2['rightMotorReverse']

    constSpeed = docDict1['constSpeed']

    if(leftStatus and rightStatus):
        print('both motor running')
        print("motor1 speed: " + str(leftMotorSpeed))
        print('motor2 speed: '+ str(rightMotorSpeed))
        motor1.LeftSide(leftMotorSpeed)
        motor2.RightSide(rightMotorSpeed)
    
    elif(leftStatus):
            print("leftMotorOn")
            motor1.LeftSide(leftMotorSpeed)
            motor2.stopMotor()
           
    elif(leftMotorReverse and rightMotorReverse):
        print('motor reverse')
        motor1.leftSideReverse(100)
        motor2.rightSideReverse(100)

    elif(rightStatus):
            print("rightMotorOn")
            motor2.RightSide(rightMotorSpeed)
            motor1.stopMotor()
               
    elif(constSpeed):
        print('const speed')
        motor1.sameSpeed()
        motor2.sameSpeed()

    else:
        print("stoping motor")
        motor1.stopMotor()
        motor2.stopMotor()
       