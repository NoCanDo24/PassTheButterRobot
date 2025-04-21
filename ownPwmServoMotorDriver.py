from gpiozero import PWMOutputDevice
from time import sleep

pwm = PWMOutputDevice(17)
pwm.frequency = 50

while True:
    try:
        pwm.value = 0.13 # duty cycle of 2.6ms (max)
        sleep(1)
        pwm.value = 0.03 # duty cycle of 0.6ms (min)
        sleep(1)
        pwm.value = 0.08 # duty cycle of 1.5ms (mid)
        sleep(1)


    except KeyboardInterrupt:
        print("Program Stopped")
        break
