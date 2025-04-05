from gpiozero import Servo
from time import sleep

myGPIO = 17

myServo = Servo(myGPIO)
try:
    while True:
        myServo.min()
        sleep(1)
        myServo.max()
        sleep(1)
except KeyboardInterrupt:
    print("Program stopped")
