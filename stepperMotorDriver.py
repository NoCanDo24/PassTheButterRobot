
from gpiozero import OutputDevice, PWMOutputDevice
from time import sleep

# Pin Definitions
IN1 = OutputDevice(12)
IN2 = OutputDevice(16)
IN3 = OutputDevice(20)
IN4 = OutputDevice(21)
ENA = PWMOutputDevice(7)  # ENA for Motor 1
ENB = PWMOutputDevice(8)  # ENB for Motor 2

# Define step sequence for the motor
step_sequence = [
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 1],
    [1, 0, 0, 1]
]

reversed_step_sequence = [
    [1, 0, 0, 1],
    [0, 0, 1, 1],
    [0, 1, 1, 0],
    [1, 1, 0, 0]
]

def set_step(w1, w2, w3, w4):
    IN1.value = w1
    IN2.value = w2
    IN3.value = w3
    IN4.value = w4

def step_motor(steps, direction=1, delay=0.01):
    ENA.value = 1  # Enable Motor 1
    ENB.value = 1  # Enable Motor 2
    for _ in range(steps):
        for step in (step_sequence if direction > 0 else reversed_step_sequence):
            set_step(*step)
            sleep(delay)
    ENA.value = 0  # Disable Motor 1
    ENB.value = 0  # Disable Motor 2

try:
    while True:
        steps = 50
        direction = int(input("Enter direction (1 for forward, -1 for backward): "))
        step_motor(steps, direction)
except KeyboardInterrupt:
    print("Program stopped by user")