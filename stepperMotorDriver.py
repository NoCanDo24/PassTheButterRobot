
from gpiozero import OutputDevice
from time import sleep
import math

# Pin Definitions
step = OutputDevice(17)
dir = OutputDevice(27)
delay = 0.05

def step(steps):
    steps = int(steps)
    if steps >= 0:
        dir.value = 1
    else:
         dir.value = 0
    
    for i in range(abs(steps)):
            step.value = 1
            sleep(delay)
            step.value = 0
            sleep(delay)


try:
    while True:
        steps = 50
        direction = int(input("Enter direction (1 for forward, -1 for backward): "))
        step(steps*math.copysign(1, direction))
        print(dir.value)
except KeyboardInterrupt:
    print("Program stopped by user")
