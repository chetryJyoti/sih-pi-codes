# relay control

import time

import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.LOW)

time.sleep(0.25)

GPIO.output(21, GPIO.HIGH)
GPIO.cleanup()