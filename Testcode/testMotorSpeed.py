import RPi.GPIO as GPIO 
from time import sleep 


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

pwm1 = GPIO.PWM(Ena1,100)
pwm1.start(0)

pwm2 = GPIO.PWM(Ena2,1000)
pwm2.start(0)



while True:
       GPIO.output(In3,GPIO.LOW)
       GPIO.output(In4,GPIO.HIGH)
    #    pwm2.ChangeDutyCycle(0)
    #    sleep(3)
    #    pwm2.ChangeDutyCycle(60)
    #    sleep(3)
    #    pwm2.ChangeDutyCycle(80)
    #    sleep(3)
      
       pwm2.ChangeDutyCycle(100)
        
       pwm1.ChangeDutyCycle(100)

