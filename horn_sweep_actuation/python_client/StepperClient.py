import serial
import time

class StepperClient():
    def __init__(self,port,baudrate):
        self.arduino = serial.Serial(port=port)
        self.arduino.baudrate = baudrate
        self.arduino.bytesize = 8 
        self.arduino.parity = 'N'
        self.arduino.stopbits = 1
        print("Connecting. Please Reset your Arduino.")
        time.sleep(3)
        rec_init = self.arduino.readline().strip()
        if rec_init == b'R':
            print("Connection Ready")
        else:
            print("Connection Failed. Received: {}".format(rec_init))
    def set_pos(self,pos):

        self.arduino.write(bytes(str(pos)+'\n','utf-8'))
        rec = self.arduino.readline().decode('utf-8').strip()
        if rec == 'DONE':
            #print("Move Completed")
            return True
        elif rec == 'OoB':
            print("Input angle out of bounds (0-360)")
            return False
    def close(self):
        self.arduino.close()
def main():
    stepper = StepperClient('/dev/ttyUSB0',115200)
    stepper.set_pos(0)
    input("Press Enter to close.")
    stepper.set_pos(90)
    input("Press Enter to close.")

    stepper.set_pos(0)
    stepper.close()
    #for pos in [0,90,180]:
    #    stepper.set_pos(pos)


if __name__ == '__main__':
    main()