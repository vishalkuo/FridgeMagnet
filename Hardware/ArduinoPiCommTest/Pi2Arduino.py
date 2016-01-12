import serial
ser = serial.Serial('/dev/ttyACM0', 9600)
ser.write('5')
while 1:
    line = ser.readline()
    if line == "1\r\n":
	break


print("End program")
