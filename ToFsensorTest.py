import serial
import time

# Connect to Pi's UART port
ser = serial.Serial('/dev/serial0', 115200)

def parse_data(data):
	if data[0] == 0x59 and data[1] == 0x59:
		distance = data[2] + data[3] * 256
		return distance
	else:
		ser.read(1)
	return None
	

ser.reset_input_buffer()

while True:
	
	if ser.in_waiting >= 9:
		raw = ser.read(9)
		distance = parse_data(raw)
		if distance:
			print(f"Distance: {distance} cm")
	time.sleep(0.005)
