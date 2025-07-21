import time
import serial # Import the pyserial library
from TMC_2209.TMC_2209_StepperDriver import TMC_2209
from gpiozero import DigitalOutputDevice

# --- GPIO Pin Definitions (BCM numbering) ---
DIR_PIN = 20
STEP_PIN = 21
ENABLE_PIN = 16 # TMC2209 EN pin is typically active low

# --- UART Configuration ---
UART_PORT = "/dev/ttyAMA0" # This is UART0 on Raspberry Pi GPIO
BAUD_RATE = 115200       # Standard baud rate for TMC2209 UART

# --- Stepper Motor Parameters ---
MOTOR_STEPS_PER_REVOLUTION = 200 # Standard for a NEMA17 motor

# --- TMC2209 R_SENSE Resistor ---
# IMPORTANT: Check your TMC2209 board for the value of the sense resistor.
R_SENSE_VALUE = 0.11 # <--- ADJUST THIS VALUE IF YOUR BOARD IS DIFFERENT!

# --- Initialize GPIO Zero for control pins ---
enable_gpio = DigitalOutputDevice(ENABLE_PIN, active_high=False) # EN is active low
dir_gpio = DigitalOutputDevice(DIR_PIN)
step_gpio = DigitalOutputDevice(STEP_PIN)

# --- Define the serial port object (will be opened in try block) ---
ser = None # Initialize to None

try:
    # --- OPEN THE SERIAL PORT DIRECTLY USING PYSERIAL ---
    print(f"Opening serial port {UART_PORT} at {BAUD_RATE} baud...")
    ser = serial.Serial(UART_PORT, BAUD_RATE, timeout=0.1) # Add a timeout for reading
    if not ser.isOpen():
        ser.open()
    print("Serial port opened successfully.")

    # --- Initialize TMC2209 Driver (UPDATED AGAIN!) ---
    # Now, pass the opened pyserial object 'ser' to the constructor.
    # The library will use this object for communication.
    tmc = TMC_2209(
        ser,                 # Pass the serial port object
        R_SENSE=R_SENSE_VALUE # R_SENSE might still be expected for current calculations
    )

    print("Enabling TMC2209 driver...")
    enable_gpio.on() # Manually enable the driver (sets EN pin LOW)
    time.sleep(0.5) # Give driver time to power up and configure

    # --- Configure TMC2209 via UART ---
    MOTOR_RATED_CURRENT_MA = 1000
    target_current_ma = int(MOTOR_RATED_CURRENT_MA * 0.6)

    print(f"Setting motor run current to {target_current_ma}mA...")
    tmc.setCurrent(target_current_ma)
    print(f"Actual current set: {tmc.getCurrent()}mA")

    MICROSTEP_RESOLUTION = 64
    print(f"Setting microstepping resolution to 1/{MICROSTEP_RESOLUTION}...")
    tmc.setMicrosteppingResolution(MICROSTEP_RESOLUTION)
    print(f"Actual microstepping: 1/{tmc.getMicrosteppingResolution()}")

    print("Enabling StealthChop2 for silent operation...")
    tmc.setStealthChop(True)

    time.sleep(1) # Give some time after configuration

    # --- Movement Functions (NOW FULLY MANUAL STEPPING) ---
    # Since the library doesn't control step/dir pins, we pulse them manually
    def move_steps_uart_config(num_steps, direction, step_delay_s=0.0005):
        # Set direction via UART (this is still possible and recommended for TMC2209)
        # Even though we're manually pulsing, setting it via UART ensures the driver's internal state is correct.
        if direction == 'clockwise':
            tmc.setDirection_reg(True)
            dir_gpio.on() # Also set the physical DIR pin for good measure if needed by some driver interpretations
        else:
            tmc.setDirection_reg(False)
            dir_gpio.off() # Also set the physical DIR pin

        time.sleep(0.0001) # Small delay for DIR to settle

        print(f"Moving {num_steps} steps {direction} (via UART config + manual pulses)...")
        for _ in range(num_steps):
            step_gpio.on()
            time.sleep(step_delay_s)
            step_gpio.off()
            time.sleep(step_delay_s)

    # --- Perform movements ---
    move_steps_uart_config(MOTOR_STEPS_PER_REVOLUTION * MICROSTEP_RESOLUTION, 'clockwise', step_delay_s=0.001)
    time.sleep(1)

    move_steps_uart_config(MOTOR_STEPS_PER_REVOLUTION * MICROSTEP_RESOLUTION // 2, 'counter-clockwise', step_delay_s=0.0005)
    time.sleep(1)

    # Note: `moveByVelocity` and `setRPM` might not work with this library
    # if it doesn't automatically generate step pulses. You'd implement
    # continuous movement by looping `step_gpio.on()/off()` indefinitely.
    print("\nUART configuration complete. Manual stepping is now active.")


except serial.SerialException as e:
    print(f"Serial port error: {e}. Make sure UART is enabled and /dev/ttyS0 exists and is accessible.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    # Print a more detailed traceback for debugging
    import traceback
    traceback.print_exc()
finally:
    print("Disabling stepper motor driver and cleaning up...")
    enable_gpio.off() # Manually disable the driver
    enable_gpio.close()
    dir_gpio.close()
    step_gpio.close()
    if ser and ser.isOpen(): # Close serial port if it was opened
        ser.close()
        print("Serial port closed.")
    print("Cleanup complete.")
