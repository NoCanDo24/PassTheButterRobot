from gpiozero import DigitalInputDevice

right_a = DigitalInputDevice(5)
right_b = DigitalInputDevice(6)
left_a = DigitalInputDevice(24)
left_b = DigitalInputDevice(23)

right_a.when_activated = handle_encoder_right
right_a.when_deactivated = handle_encoder_right
right_b.when_activated = handle_encoder_right
right_b.when_deactivated = handle_encoder_right

left_a.when_activated = handle_encoder
left_a.when_deactivated = handle_encoder
left_b.when_activated = handle_encoder
left_b.when_deactivated = handle_encoder

pulse_count = 0

def handle_encoder_right():

    print(f"[{right_a.value}, {right_b.value}]")

    # if right_a.is_active:
    #     if right_b.is_active:
    #         pulse_count -= 1
    #     else:
    #         pulse_count += 1
    # else:
    #     if right_b.is_active:
    #         pulse_count += 1
    #     else:
    #         pulse_count.is_active: