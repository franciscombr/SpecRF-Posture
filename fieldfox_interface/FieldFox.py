import pyvisa
import time
import sys
import numpy as np
#import dataprocessing

class FieldFox:

    def __init__(self):
        self.session = None

    def connect_to_vna(self,visa_adress):
        print("Attempting to connect to FieldFox...")

        resource_manager = pyvisa.ResourceManager()

        try:
            new_session = resource_manager.open_resource(visa_adress)
            if new_session is not None:
                print("Connected!")
                new_session.read_termination = '\n'
                new_session.write_termination = '\n'
                new_session.timeout = 10000
                self.session = new_session
                return True
        except:
            print("Failed to connect to FieldFox. Check that it is on and connected.")
            return False
    
    def set_vna_to_network_analyzer_mode(self):
        self.session.write('INST "NA";*OPC?')
        network_analyzer_set_success = False
        network_analyser_set_loop_count = 0

        while not network_analyzer_set_success:
            if network_analyser_set_loop_count == 10:
                print("Setting FieldFox mode Failed. Program will now close.")
                sys.exit()
            
            try:
                network_analyzer_set_success = self.session.read()
                print("VNA set to NA mode. Configuring settings...")
                time.sleep(1)
                
                #Set VNA to not continuous mode
                self.session.write('INIT:CONT OFF;*OPC?')
                self.session.read()
                time.sleep(1)
                
                #Tells vna to show only 1 S parameter measurement
                self.session.write('CALC:PAR:COUN 1')
                time.sleep(1)

                print("VNA Ready")
                time.sleep(1)
                return 1
            except:
                print("Waiting for FieldFox to be set to NA mode...(" + str(10-network_analyser_set_loop_count) + " attemps remaining)")
            
            network_analyser_set_loop_count += 1
            time.sleep(1)
    
    def set_vna_s_parameter_to_measure(self,SXX='S21'):
        self.session.write("CALC:PAR:DEF "+ SXX + ";*OPC?")
        if self.session.read():
            print("FieldFox set to measure " + SXX + " parameter.")
            return 1 
        else:
            print("Failed to set measurement of " + SXX + " parameter.")
            return -1
    
    def set_vna_sweep_range(self,steps, start=None,end=None, center=None, span=None):
        if (start is not None or end is not None) and (center is not None or span is not None):
            raise ValueError("Specify either (start, end) or (center, span), but not both.")
        elif (start is None or end is None) and (center is None or span is None):
            raise ValueError("Specify either (start, end) or (center, span).") 
        elif (start is not None and end is not None):
            self.session.write("FREQ:STAR "+str(start))
            self.session.write("FREQ:STOP "+str(end))
        elif (center is not None and span is not None):
            self.session.write("FREQ:CENT "+str(center))
            self.session.write("FREQ:SPAN "+str(span))
        
        self.session.write("SWE:POIN "+str(steps))

        return self.get_vna_sweep_range()

    def get_vna_sweep_range(self):
        self.session.write("FREQ:DATA?")
        return np.fromstring(self.session.read(),dtype=int,sep=',')
    
    def set_vna_measurement_averages(self,avgs,mode=None):
        if avgs<=10000 and avgs>=1:
            self.session.write("AVER:COUN "+str(avgs))
        else:
            raise ValueError("Number of averages must be between 1 and 10000")

        if mode=='SWEEP' or mode is None:
            self.session.write("AVER:MODE SWE")
        elif mode=='POINT':
            self.session.write("AVER:MODE POINT")
        else:
            raise ValueError("Averaging mode can be either 'SWEEP' or 'POINT'")

    def take_raw_measurement(self):
        while True:
            self.session.write("INIT:IMM;*OPC?")
            #print("Single Tigger complete, *OPC? returned:" + self.session.read())
            self.session.read()
            self.session.write("DISP:WIND:TRAC1:Y:AUTO")
            self.session.write("CALC:DATA:SDAT?")
            res = np.fromstring(self.session.read(),dtype=float,sep=',')
            if len(res) == len(self.get_vna_sweep_range())*2: 
                break
            else:
                print("Acquisition failed. Repeating...")
                continue

        return res 
    
    def take_formated_measurement(self):
        self.session.write("INIT:IMM;*OPC?")
        print("Single Tigger complete, *OPC? returned:" + self.session.read())
        self.session.write("DISP:WIND:TRAC1:Y:AUTO")

        self.session.write("CALC:DATA:FDAT?")
        return np.fromstring(self.session.read(),dtype=float, sep=',')

    def get_magnitude(self):
        self.set_data_format('MLOG')
        return self.take_formated_measurement() 
    
    def get_phase(self):
        self.set_data_format('PHAS')
        return self.take_formated_measurement()

    def get_data_format(self):
        self.session.write("CALC:FORM?")
        print("Reading data in "+self.session.read()+" format.")
    
    def set_data_format(self,d_format):
        self.session.write("CALC:FORM "+d_format+";*OPC?")
        self.session.read()
        self.get_data_format()
    
    def select_parameter(self,n):
        self.session.write("CALC:PAR"+str(n)+":SEL;*OPC?")
        print("Trace selected, *OPC? returned:" + self.session.read())
    

        
    def disconnect(self):
        self.session.clear()
        self.session.close()
        print("closing")


def main():
    my_ffox = FieldFox()
    my_ffox.connect_to_vna('USB0::0x2A8D::0x5C18::MY57271394::0::INSTR')
    my_ffox.set_vna_to_network_analyzer_mode()
    my_ffox.set_vna_s_parameter_to_measure('S21')
    #sweep = my_ffox.set_vna_sweep_range(10,center=3e6, span=1e3)
    #my_ffox.set_vna_measurement_averages(100,'SWEEP')
    my_ffox.select_parameter(1)
    meas = []
    meas.append(np.reshape(my_ffox.take_raw_measurement(),(-1,2)))
    meas.append(np.reshape(my_ffox.take_raw_measurement(),(-1,2)))
    
    dataprocessing.format_raw_meas(meas,my_ffox.get_vna_sweep_range(),np.array([0,20]),'test.csv')

    #my_ffox.disconnect()
    return

if __name__ == '__main__':
    main()

