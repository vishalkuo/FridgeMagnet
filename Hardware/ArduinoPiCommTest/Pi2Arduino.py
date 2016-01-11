import serial
ser = serial.Serial('/dev/ttyACM0', 9600)
ser.write('5')
while 1:
    line = ser.readline()
    print(line)
    if line == 'Done!':
	print line
	break

print("End program")
