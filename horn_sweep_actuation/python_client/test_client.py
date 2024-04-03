import serial 
import time 
arduino = serial.Serial(port='/dev/ttyUSB0')
arduino.baudrate = 115200
arduino.bytesize = 8
arduino.parity='N'
arduino.stopbits = 1
time.sleep(3) 
def write_read(x): 
   arduino.write(bytes(x+'\n','utf-8')) 
   data = arduino.readline()
   return data 
while True: 
   num = input("Enter a number: ") # Taking input from user 
   value = write_read(num) 
   print(value) # printing the value 
