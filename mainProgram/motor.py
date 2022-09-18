from xmlrpc.client import boolean
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


reverseMotorS=False
speedS=0
turnSpeedS=0
increaseSpeedS=False
decreaseSpeedS=False
startedS=False

# capturing changes in the database
def on_snapshot(doc_snap,changes,read_time):
    for doc in doc_snap:
        docDict = doc.to_dict()
        reverseMotor=docDict['reverseMotor']
        speed=docDict['speed']
        started=docDict['started']
        turnSpeed=docDict['turnSpeed']
        decreaseSpeed=docDict['decreaseSpeed']
        increaseSpeed=docDict['increaseSpeed']
        global reverseMotorS,speedS,turnSpeedS,increaseSpeedS,decreaseSpeedS,startedS
        reverseMotorS=reverseMotor
        speedS=speed
        startedS=started
        turnSpeedS=turnSpeed
        increaseSpeedS=increaseSpeed
        decreaseSpeedS=decreaseSpeed
       
    callback_done.set()

doc_ref = db.collection('PMotor').document('motors')

# watch the document

doc_watch = doc_ref.on_snapshot(on_snapshot)

# main class
class Motor():
    def __init__(self, EnaA, In1A, In2A, EnaB, In1B, In2B):
        self.EnaA = EnaA
        self.In1A = In1A
        self.In2A = In2A
        self.EnaB = EnaB
        self.In1B = In1B
        self.In2B = In2B
        GPIO.setup(self.EnaA, GPIO.OUT)
        GPIO.setup(self.In1A, GPIO.OUT)
        GPIO.setup(self.In2A, GPIO.OUT)
        GPIO.setup(self.EnaB, GPIO.OUT)
        GPIO.setup(self.In1B, GPIO.OUT)
        GPIO.setup(self.In2B, GPIO.OUT)
        self.pwmA = GPIO.PWM(self.EnaA, 100)
        self.pwmA.start(0)
        self.pwmB = GPIO.PWM(self.EnaB, 100)
        self.pwmB.start(0)

    def move(self, speed=1, turn=0, t=0):
        speed *= 100
        turn *= 100
        leftSpeed = speed - turn
        rightSpeed = speed + turn
        if leftSpeed > 100:
            leftSpeed = 100
        elif leftSpeed < -100:
            leftSpeed = -100
        if rightSpeed > 100:
            rightSpeed = 100
        elif rightSpeed < -100:
            rightSpeed = -100

        print("rightspeed:"+str(rightSpeed))
        self.pwmB.ChangeDutyCycle(abs(rightSpeed))
        print("leftspeed:"+str(leftSpeed))
        self.pwmA.ChangeDutyCycle(abs(leftSpeed))

        if leftSpeed > 0:
            print('left clock')
            GPIO.output(self.In1A, GPIO.HIGH)
            GPIO.output(self.In2A, GPIO.LOW)
        else:
            print('left anti')
            GPIO.output(self.In1A, GPIO.LOW)
            GPIO.output(self.In2A, GPIO.HIGH)

        if rightSpeed > 0:
            print('right clock')
            GPIO.output(self.In1B, GPIO.LOW)
            GPIO.output(self.In2B, GPIO.HIGH)

        else:
            print('right anti')
            GPIO.output(self.In1B, GPIO.HIGH)
            GPIO.output(self.In2B, GPIO.LOW)

        sleep(t)

    def stop(self, t=0):
        self.pwmA.ChangeDutyCycle(0)
        self.pwmB.ChangeDutyCycle(0)
        sleep(t)

    def reverse(self, reverseSpeed=100, t=0):
        # print("rightspeed:"+str(rightSpeed))
        self.pwmB.ChangeDutyCycle(abs(reverseSpeed))
        # print("leftspeed:"+str(leftSpeed))
        self.pwmA.ChangeDutyCycle(abs(reverseSpeed))
        GPIO.output(self.In1A, GPIO.LOW)
        GPIO.output(self.In2A, GPIO.HIGH)
        GPIO.output(self.In1B, GPIO.HIGH)
        GPIO.output(self.In2B, GPIO.LOW)


def main():
    # MotorData = db.collection('PMotor').document('motors').get()
    # docDict1 = MotorData.to_dict()
    # motorSpeed = docDict1['speed']
    # motorTurnSpeed = docDict1['turnSpeed']
    # motorReverseStatus = docDict1['reverseMotor']
    # print(motorSpeed)
    # print(motorTurnSpeed)
    # starting motor
    if (speedS == 1 and startedS):
        motor.move()

    # stoping motor
    elif (speedS == 0 ):
        motor.stop()

    elif (reverseMotorS and speedS>0):
        motor.reverse()

    elif (increaseSpeedS):
        motor.move(speedS)
        
    elif (decreaseSpeedS):
        motor.move(speedS)

    elif (turnSpeedS):
        motor.move(speedS,turnSpeedS)


    


if __name__ == '__main__':
    motor = Motor(2, 3, 4,17,22,27)
    while True:
        main()
