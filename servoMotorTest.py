from gpiozero import AngularServo
from time import sleep

myGPIO = 17

myServo = AngularServo(myGPIO, min_angle=-50, max_angle=70)
try:
    while True:
        myServo.angle = -50
        sleep(1)
        myServo.angle = 70
        sleep(1)
except KeyboardInterrupt:
    print("Program stopped")
