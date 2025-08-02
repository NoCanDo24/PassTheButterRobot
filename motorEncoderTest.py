from gpiozero import DigitalInputDevice
from signal import pause

right_a = DigitalInputDevice(5)
right_b = DigitalInputDevice(6)
left_a = DigitalInputDevice(24)
left_b = DigitalInputDevice(23)


old_phase = None
new_phase = None
pulse_count = 0

def handle_encoder_right():

    if old_phase ==  None:
        old_phase = bin(right_a.value + 2* right_b.value)

    new_phase = bin(right_a.value + 2* right_b.value)

    if old_phase == new_phase >> 1:
        pulse_count += 1
    elif old_phase == new_phase << 1:
        pulse_count -= 1

    print(bin(right_a.value + 2* right_b.value))

    # if right_a.is_active:
    #     if right_b.is_active:
    #         pulse_count -= 1
    #     else:
    #         pulse_count += 1
    # else:
    #     if right_b.is_active:
    #         pulse_count += 1
    #     else:
    #         pulse_count -= 1

right_a.when_activated = handle_encoder_right
right_a.when_deactivated = handle_encoder_right
right_b.when_activated = handle_encoder_right
right_b.when_deactivated = handle_encoder_right

pause()

# left_a.when_activated = handle_encoder
# left_a.when_deactivated = handle_encoder
# left_b.when_activated = handle_encoder
# left_b.when_deactivated = handle_encoder