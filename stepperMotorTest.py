from gpiozero import DigitalOutputDevice, LED # LED can be used for simple output like EN
import time

# --- GPIO Pin Definitions (BCM numbering) ---
DIR_PIN = 27
STEP_PIN = 17
ENABLE_PIN = 22 # TMC2209 EN pin is typically active low

# --- Initialize GPIO Zero devices ---
dir_pin = DigitalOutputDevice(DIR_PIN)
step_pin = DigitalOutputDevice(STEP_PIN)
enable_pin = DigitalOutputDevice(ENABLE_PIN, active_high=False) # Set active_high=False for EN

# --- Stepper Motor Parameters ---
# Steps per revolution for your motor (e.g., 200 for a NEMA17)
# Microstepping: If you've set jumpers for 1/16 microstepping, then steps_per_revolution * 16
MOTOR_STEPS_PER_REVOLUTION = 200
MICROSTEPPING_RESOLUTION = 16 # Example: 1/16 microstepping
TOTAL_STEPS_PER_REVOLUTION = MOTOR_STEPS_PER_REVOLUTION * MICROSTEPPING_RESOLUTION

# --- Movement Functions ---
def move_steps(num_steps, direction, step_delay_s=0.0005):
    if direction == 'clockwise':
        dir_pin.off() # Or .value = 1
    elif direction == 'counter-clockwise':
        dir_pin.on() # Or .value = 0
    else:
        print("Invalid direction. Use 'clockwise' or 'counter-clockwise'.")
        return
    print(f"DEBUG: Direction set to {dir_pin.value} for {direction}")
    print(f"Moving {num_steps} steps {direction}...")
    for _ in range(num_steps):
        step_pin.on()
        time.sleep(step_delay_s)
        step_pin.off()
        time.sleep(step_delay_s)

try:
    print("Enabling stepper motor driver...")
    enable_pin.on() # `on()` will set it LOW because active_high=False

    time.sleep(0.5) # Give driver time to enable

    # Example movements
    print("\nMoving 1 revolution clockwise...")
    move_steps(TOTAL_STEPS_PER_REVOLUTION, 'clockwise', step_delay_s=0.001) # Slower speed
    time.sleep(1)

    print("\nMoving 0.5 revolution counter-clockwise...")
    move_steps(int(TOTAL_STEPS_PER_REVOLUTION / 2), 'counter-clockwise', step_delay_s=0.001) # Faster speed
    time.sleep(1)

    print("\nMoving 200 microsteps clockwise (short move)...")
    move_steps(200, 'clockwise', step_delay_s=0.001) # Even faster
    time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping motor.")
finally:
    print("Disabling stepper motor driver and cleaning up GPIO...")
    enable_pin.off() # `off()` will set it HIGH because active_high=False, disabling the driver
    dir_pin.close()
    step_pin.close()
    enable_pin.close()
    print("GPIO cleanup complete.")
