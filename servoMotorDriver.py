from gpiozero import PWMOutputDevice


class ServoMotor:

    def __init__(self, pin, frequency=50, min_cycle=0.5, max_cycle=2.5, angle_range=270):
        self.pin = pin
        self.pwm = PWMOutputDevice(pin)
        self.frequency = frequency
        self.pwm.frequency = frequency

        self.min = min_cycle
        self.max = max_cycle

        self.angle_range = angle_range

        
    
    def updateAngle(self, angle):
        ms = angle * (self.max - self.min)/self.angle_range + self.min
        self.pwm.value = self.msToValue(ms)

    def msToValue(self, ms):
        return ms*0.001*self.frequency

s = ServoMotor(2)
while True:
    try:
        angleInput = int(input("What angle do you want?"))
        s.updateAngle()



    except KeyboardInterrupt:
        print("Program Stopped")
        break
