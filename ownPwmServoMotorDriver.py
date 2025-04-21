from gpiozero import PWMOurputDevice

pwm = PWMOurputDevice(17)
pwm.frequency = 50

while True:
    try:
        # pwm.value = 0.1 # duty cycle of 2ms (max)
        # pwm.value = 0.05 # duty cycle of 1ms (min)
        pwm.value = 0.075 # duty cycle of 1.5ms (mid)


    except KeyboardInterrupt:
        print("Program Stopped")
        break