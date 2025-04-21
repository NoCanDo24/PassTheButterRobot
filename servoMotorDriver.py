from gpiozero import PWMOutputDevice


class ServoMotor:

    def __init__(self, pin, frequency=50, min_cycle=0.03, mid_cycle=0.08, max_cycle=0.13, min_angle=-90, max_angle=90):
        self.pin = pin
        self.pwm = PWMOutputDevice(pin)
        self.frequency = frequency
        self.pwm.frequency = frequency

        self.min = min_cycle
        self.mid = mid_cycle
        self.max = max_cycle

        self.min_angle = min_angle
        self.max_angle = max_angle

        self.pwm.value = self.mid
    
    def updateAngle(self, angle):
        if angle >= self.min_angle and angle <= self.max_angle:
            duty_cycle = self.angleToDutycycle(angle)

    def angleToDutycycle(self, angle):
        return 0


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
