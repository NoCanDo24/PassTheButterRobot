from gpiozero import PWMOutputDevice, OutputDevice

IN1 = OutputDevice(11)
IN2 = OutputDevice(9)
IN3 = OutputDevice(10)
IN4 = OutputDevice(22)
ENA = PWMOutputDevice(8)
ENB = PWMOutputDevice(25)

def drive(speed):
    if abs(speed) > 1:
        return
    ENA.value = abs(speed)
    ENB.value = abs(speed)
    if speed >= 0:
        IN1.value = 1
        IN2.value = 0
        IN3.value = 1
        IN4.value = 0
    else:
        IN1.value = 0
        IN2.value = 1
        IN3.value = 0
        IN4.value = 1

while True:
    try:
        input = input("I am SPEED?:")
        drive(input)



    except KeyboardInterrupt:
        print("Program Stopped")
        break