import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)
line_buffer_wait = 1

def hold():
    time.sleep(line_buffer_wait)

def clear_LCD():
    ser.write("0" + "x")

def write_to_LCD(line_1, line_2):
    clear_LCD()
    hold()
    ser.write("0" + line_1)
    hold()
    ser.write("1" + line_2)
