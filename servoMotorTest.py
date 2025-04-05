from gpiozero import Servo
from time import sleep

myGPIO = 17

myCorrection = 0.45
maxPW = (2.0+myCorrection)/1000
minPW = (1.0-myCorrection)/1000

myServo = Servo(myGPIO, min_pulse_width=minPW, max_pulse_width=maxPW)
try:
    while True:
        myServo.min()
        sleep(1)
        myServo.max()
        sleep(1)
except KeyboardInterrupt:
    print("Program stopped")
