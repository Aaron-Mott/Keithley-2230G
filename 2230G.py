# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:07:47 2020

@author: Aaron Mott
aaron.b.mott@gmail.com
"""


import visa
import numpy

class KEI2230G():
    
    def __innit__(self):
        
        self.rm = visa.ResourceManager()
        #self.inst_address = 
        baud_rate = 9600 #Can be set to 4800, 9600, 19200, 38400, 57600, 115200
        self.inst = self.rm.open_resource(self.instr_address, baud_rate)
        self.inst.term_chars = '/n'
        self.inst.timeout = None
        
        #Clear all the event registers and error queue.  
    def clear_status(self):
        
        self.inst.write("*CLS")
        
        #Edit the Standard Event Enable Register.  
    def edit_standard_event(self, NRf):

        self.inst.write(f"*ESE {NRf}")
        
        #Read the Standard Event Enable Register.  
    def get_standard_event(self):
        
        current_register = str(self.inst.query("*ESE?"))
        return(current_register)
        
        #Read the Standard Event Status Register and clear it.  
    def get_standard_event_and_clear(self):
        
        current_register = str(self.inst.query("*ESR?"))
        return(current_register)
        
        #Return the instrument manufacturer, model, serial number,
        #and firmware revision level.  
    def get_info(self):
        
        info = str(self.inst.query("*IDN?")).split(',')
        return(" Manufacturer: " + info[0] + '\n',
              "Model: " + info[1] + '\n',
              "Serial Number: " + info[2]+'\n',
              " Firmware Version: " + info[3])
    
        #Returns model type (30-3, 30-6, or 60-3).  
    def get_model(self):
        
        model = (str(self.get_info.split('\n')[1].split(":")
                     [1].replace(" ", ""))[6:10])
        return(model)
        
        #Set the Operation Complete bit in the Standard Event Status Register
        #to 1 after all pending commands have been executed.  
    def set_op_complete(self):
        
        self.inst.write("*OPC")
        
        #Indicates whether all pending OPC operations are finished.  
    def get_op_complete(self):
        
        op = self.inst.query("*OPC?")
        if int(op) == 1:
            return("All OPC operations are finished.")
        else:
            return("Some OPC operations are still ongoing.")
            
        #This command specifies sets the power status clear flag to true
        #or false. 0 is false and 1 is true.
    def set_psc(self, NR1):
        
        if int(NR1) in range(2):
            self.inst.write(f"*PSC {NR1}")
        else:
            raise ValueError("Value Error. Please enter 0 for false or 1 for "
                             "true.")
        
        #Recalls the setups you saved in the specified memory location.  
    def set_setup(self, NR1):
        
        if int(NR1) in range(1, 37):
            self.inst.write(f"*RCL {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between 1 "
                             "and 36.")
            
        #Resets the power supply to default settings.  
    def reset_settings(self):
        
        self.inst.write("*RST")
        
        #Saves the present current, voltage, and maximum voltage settings
        #of the power supply into specified memory.  
    def save_to(self, NR1):
        
        if int(NR1) in range(1, 37):
            self.inst.write(f"*SAV {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between 1 "
                             "and 36.")
        
        #Sets or the bits in the Status Byte Enable Register.  
    def set_status_byte(self, NR1):
        
        if int(NR1) in range(256):
            self.inst.write(f"*SRE {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between 0 "
                             "and 255.")
        
        #Queries Status Byte Enable Register.  
    def get_status_byte(self):
        
        status_byte = str(self.inst.query("*SRE"))
        return(status_byte)
    
        #Reads the data in the Status Byte Register.  
    def get_sbr(self):
        
        sbr = str(self.inst.query("*STB"))
        return(sbr)
    
        #Initiates a self-test and reports any errors.  
    def self_test(self):
        
        error_code = str(self.inst.query("*TST"))
        return(error_code)
    
        #Prevents the instrument from executing further commands or queries
        #until all pending commands are complete.  
    def wait(self):
        
        self.inst.write("*WAI")
    
        #Clears the calibration information on the instrument.  
    def cal_cle(self):
        
        self.inst.write("CAL:CLE")
        
        #Sets the actual output current value of the calibration point.  
    def cal_curr(self, NR2):
        
        if type(NR2) is float or int:
            self.inst.write(f"CAL:CURR {NR2}")
        else:
            raise ValueError("Value Error. Please refer to the manual for "
                             "correct inputs.")
        
        #Sets the current calibration points.  
    def cal_curr_lev(self, point):
        
        if str(point).upper() == 'P1' or 'P2':
            self.inst.write(f"CAL:CURR:LEV {point}.upper()")
        else:
            raise ValueError("Value Error. Please enter P1 or P2.")
        
        #Sets the current calibration coefficient as the default value.
    def cal_init(self):
        
        self.inst.write("CAL:INIT")
        
        #Saves the calibration coefficient into nonvolatile memory.  
    def cal_sav(self):
        
        self.inst.write("CAL:SAV")
        
        #Enables or disables calibration mode.  
    def cal_sec(self, boolean, password):
        
        #Gets serial number
        code = str(self.get_info.split('\n')[1].split(":")[1].replace(" ", ""))
        #Checks if state and password are correct
        if boolean in range(2) and str(password) == code:
            self.inst.write(f"CAL:SEC {boolean} {password}")
        else:
            raise ValueError("Value Error. Please refer to the manual for "
                             "correct inputs.")
        
        #Enables or disables calibration mode without asking for password.  
    def cal_sec_unsecure(self, boolean):
        
        code = str(self.get_info.split('\n')[1].split(":")[1].replace(" ", ""))
        if boolean in range(2):
            self.inst.write(f"CAL:SEC {boolean} {code}")
        else:
            raise ValueError("Value Error. Please enter 0 or 1.")
            
        #Writes the calibration information of the instrument.  
    def cal_str(self, string):
        
        if 0 <= len(str(string).encode('utf8')) <= 23:
            self.inst.write(f"CAL:STR {string}")
        else:
            raise ValueError("Value Error. Please enter a string less than 22 "
                             "bytes.")
            
        #Queries for calibration information of the intrsument.  
    def get_cal(self):
        
        cal = str(self.inst.query("CAL:STR?"))
        return(cal)
    
        #Sets the actual output voltage value of the calibration point.  
    def cal_volt(self, NR2):
        
        if (self.get_model() in ['2230G-30-3', '2230G-30-6'] and
                                0 <= float(NR2) <= 30):
            self.inst.write(f"CAL:VOLT {NR2}")
        else:
            raise ValueError("Value Error. Please refer to the manual for "
                             "correct inputs.")
        
        #Sets the voltage calibration points.  
    def cal_volt_lev(self, point):
        
        if str(point).upper() in ['P1', 'P2', 'P3', 'P4']:
            self.inst.write(f"CAL:VOLT:LEV {point}.upper()")
        else:
            raise ValueError("Value Error. Please enter P1, P2, P3, or P4.")
        
        #Queries the connection state of the channels.  
    def inst_com(self):
        
        comb = str(self.inst.query("INST:COMB?"))
        return(comb)
    
        #Turns off the connection of channels.  
    def inst_comb_off(self):
        
        self.inst.write("INST:COM:OFF")
        
        #Specifies that the instrument combines the present readings of 
        #channels when they are connected in parallel.  
    def set_parallel(self, level):
        
        if str(level).upper() in ["CH1CH2", "CH2CH3", "CH1CH2CH3"]:
            self.inst.write(f"INST:COM:PAR {level}.upper()")
        else:
            raise ValueError("Value Error. Please enter CH1CH2, CH2CH3, or "
                             "CH1CH2CH3.")
        
        #Combines the present voltage readings on channel 1 (CH1) and
        #channel 2 (CH2) when they are connected in series.
    def inst_com_ser(self):
        
        self.inst.write("INST:COMB:SER")
        
        #Sets channels to tracking mode.  
    def set_track(self, level):
        
        if str(level).upper() in ["CH1CH2", "CH2CH3", "CH1CH2CH3"]:
            self.inst.write(f"INST:COMB:TRAC {level}.upper()")
        else:
            raise ValueError("Value Error. Please enter CH1CH2, CH2CH3, or "
                             "CH1CH2CH3.")
        
        #Selects channel number.  
    def select_channel(self, NR1):
        
        if int(NR1) in range(1, 4):
            self.inst.write(f"INST:NSEL {NR1}")
        else:
            raise ValueError("Value Error. Please enter 1, 2, or 3.")
        
        #Selects the channel.  
    def set_channel(self, level):
        
        if str(level).upper() in ["CH1", "CH2", "CH3"]:
            self.inst.write(f"INST {level}.upper()")
        else:
            raise ValueError("Value Error. Please enter CH1, CH2, or CH3.")
        
        #Queries selected channel.  
    def get_channel(self):
        
        channel = str(self.inst.query("INST?"))
        return(channel)
    
        #Queries the current reading on the specified channel.  
    def get_channel_curr(self, level):
        
        if str(level).upper() in ["CH1", "CH2", "CH3", "ALL"]:
            reading = str(self.inst.query(f"FETC:CURR? {level}.upper()"))
            return(reading)
        else:
            raise ValueError("Value Error. Please enter CH1, CH2, CH3, or ALL"
                             ".")
        
        #Queries the present power measurement on a specified
        #channel or channels.  
    def get_power(self, level):
        
        if str(level).upper() in ["CH1", "CH2", "CH3", "ALL"]:
            power = str(self.inst.query(f"FETC:POW? {level}.upper()"))
            return(power)
        else:
            raise ValueError("Value error. Please enter CH1, CH2, CH3, or ALL"
                             ".")
        
        #Queries the new current voltage on a specified channel or channels.
    def get_volt(self, level):
        
        if str(level).upper() in ["CH1", "CH2", "CH3", "ALL"]:
            volt = str(self.inst.query(f"FETC:VOLT? {level}.upper()"))
            return(volt)
        else:
            raise ValueError("Value Error. Please enter CH1, CH2, CH3, or ALL"
                             ".")
        
        #Initiates and executes a new current measurement or queries the
        #new measured current on a specified channel or channels.
    def meas_curr(self, level): 
        
        if str(level).upper() in ["CH1", "CH2", "CH3", "ALL"]:
            curr_meas = str(self.inst.query(f"MEAS:CURR? {level}.upper()"))
            return(curr_meas)
        else:
            raise ValueError("Value Error. Please enter CH1, CH2, CH3, or ALL"
                             ".")
    
        #Unitiates and executes a new power measurement or
        #queries the new measured power.  
    def meas_power(self, level):
        
        if str(level).upper() in ["CH1", "CH2", "CH3", "ALL"]:
            pow_meas = str(self.inst.query(f"MEAS:POW? {level}.upper()"))
            return(pow_meas)
        else:
            raise ValueError("Value Error. Please enter CH1, CH2, CH3, or ALL"
                             ".")
        
        #Initiates and executes a new voltage measurement or
        #queries the new measured voltage.  
    def meas_volt(self, level):
        
        if str(level).upper() in ["CH1", "CH2", "CH3", "ALL"]:
            volt_meas = str(self.inst.query(f"MEAS:VOLT? {level}.upper()"))
            return(volt_meas)
        else:
            raise ValueError("Value Error. Please enter CH1, CH2, CH3, or ALL"
                             ".")
        
        #Sets voltage and current levels on a specified channel
        #with a single command message.  
    def apply_volt(self, level, volt, curr):
        
        if self.get_model == '30-3':
            if str(level.upper()) in ["CH1", "CH2"]:
                if (str(volt).upper() and str(curr).upper() in 
                    ["MAX", "MIN", "DEF", "UP", "DOWN"] or
                        0 <= float(volt) <= 31 and 0 <= float(curr) <= 4):
                        self.inst.write((f"APPL {level}.upper(), {volt}.upper,"
                                         "{curr}.upper()"))
            elif str(level.upper()) == 'CH3':
                if (str(volt).upper() and str(curr).upper() in 
                    ["MAX", "MIN", "DEF", "UP", "DOWN"] or
                    0 <= float(volt) in 0 <= 5 and 0 <= float(curr) <= 3):
                        self.inst.write((f"APPL {level}.upper(), {volt}.upper," 
                                         "{curr}.upper()"))
        if self.get_model == '30-6':
            if str(level.upper()) in ["CH1", "CH2"]:
                if (str(volt).upper() and str(curr).upper() in 
                    ["MAX", "MIN", "DEF", "UP", "DOWN"] or
                    0 <= float(volt) <= 30 and 0 <= float(curr) <= 6):
                        self.inst.write((f"APPL {level}.upper(), {volt}.upper," 
                                         "{curr}.upper()"))
            elif str(level.upper()) == 'CH3':
                if (str(volt).upper() and str(curr).upper() in 
                    ["MAX", "MIN", "DEF", "UP", "DOWN"] or
                    0 <= float(volt) <= 5 and 0 <= float(curr) <= 3):
                        self.inst.write((f"APPL {level}.upper(), {volt}.upper," 
                                         "{curr}.upper()"))
        if self.get_model == '60-3':
            if str(level.upper()) in ["CH1", "CH2"]:
                if (str(volt).upper() and str(curr).upper() in 
                    ["MAX", "MIN", "DEF", "UP", "DOWN"] or
                    0 <= float(volt) <= 60 and 0 <= float(curr) <= 3):
                        self.inst.write((f"APPL {level}.upper(), {volt}.upper," 
                                         "{curr}.upper()"))
            elif str(level.upper()) == 'CH3':
                if (str(volt).upper() and str(curr).upper() in 
                    ["MAX", "MIN", "DEF", "UP", "DOWN"] or
                    0 <= float(volt) <= 5 and 0 <= float(curr) <= 3):
                        self.inst.write((f"APPL {level}.upper(), {volt}.upper," 
                                         "{curr}.upper()"))
        else:
            raise ValueError("Value Error. Please refer to the manual for "
                             "correct inputs.")
        
        #Sets the output state of the presently selected channel.  
    def set_output(self, boolean):
        
        if str(boolean).upper() in ["ON", "OFF"]:
            self.inst.write(f"CHAN:OUTP {boolean}.upper()")
        if int(boolean) in range(2):
            self.inst.write(f"CHAN:OUTP {boolean}.upper()")
        else:
            raise ValueError("Value Error. Please enter ON, OFF, 0, or 1.")
        
        #Returns the output state of the presently selected channel.  
    def get_output(self):
        
        channel_output = str(self.inst.query("CHAN:OUTP?"))
        return(channel_output)
    
            #Sets the amount to increase current level.  
    def set_curr_step(self, step):
        
        self.inst.write("CURR:STEP " + str(step))
        
        #Returns the current step amount.
    def get_curr_step(self):
        
        curr_step = str(self.inst.query("CURR:STEP?"))
        return(curr_step)
    
        #Decreases the current value of the present channel by one step.,
        #as specified by the set_curr_step command.  
    def curr_down(self):
        
        self.inst.write("CURR:DOWN")
        
        #Increases the current value of the present channel by one step,
        #as specified by the set_curr_step command.  
    def curr_up(self):
        
        self.inst.write("CURR:UP")
        
        #Sets the current value of the power supply.  
    def set_curr(self, curr):
        
        if self.get_model == '30-3':
                if 0 <= float(curr) <= 3:
                    self.inst.write(f"CURR {curr}")
        if self.get_model == '30-6':
            if self.get_channel in ['CH1', 'CH2']:
                if 0 <= float(curr) <= 6:
                    self.inst.write(f"CURR {curr}")
            elif self.get_channel == 'CH3':
                if 0 <= float(curr) <= 4:
                    self.inst.write(f"CURR {curr}")
        if self.get_model == '60-3':
            if 0 <= float(curr) <= 3:
                self.inst.write(f"CURR {curr}")
        else:
            raise ValueError("Value Error. Please refer to the manual for "
                             "correct inputs.")
        
        #Returns the current value of the power supply.  
    def get_curr(self):
        
        curr = str(self.inst.query("CURR?"))
        return(curr)
        
        #Sets the output state of the power supply.      
    def set_output_state(self, boolean):
        
        if str(boolean).upper() in ['ON', 'OFF']:
            self.inst.write(f"OUTP:ENAB {boolean}.upper()")
        if int(boolean) in range(2):
            self.inst.write(f"OUTP:ENAB {boolean}")
        else:
            raise ValueError("Value Error. Please enter ON, OFF, 0, or 1.")
        
        #Sets the parallel synchronization state of the three channels.  
    def set_output_parrallel(self, channels):
        
        if str(channels).upper() in ['CH1CH2', 'CH2CH3', 'CH1CH2CH3']:
            self.inst.write(f"OUTP: PAR {channels}.upper()")
        else:
            raise ValueError("Value Error. Please enter CH1CH2, CH2CH3, or "
                             "CH1CH2CH3.")
        
        #Returns the parallel synchronization state of the three channels.  
    def get_output_parrallel(self):
        
        output_parrallel = str(self.inst.query("OUTP:PAR?"))
        return(output_parrallel)
    
        #Clears the protection state of the power supply.  
    def clear_state(self):
        
        self.inst.write("OUTP:PROT:CLE")
        
        #Sets the series synchronization state of channel 1 (CH1)
        #and channel 2 (CH2). If channel 3 (CH3) and CH1 or CH3 and CH2 are
        #in parallel synchronization states, an error is generated after
        #the command is executed.  
    def set_output_series(self, boolean):
        
        if str(boolean).upper() in ['ON', 'OFF']:
            self.inst.write(f"OUTP:SER {boolean}.upper()")
        if int(boolean) in range(2):
            self.inst.write(f"OUTP:SER {boolean}")
        else:
            raise ValueError("Value Error. Please enter ON, OFF, 0, or 1.")
        
        #Returns the synchronization state of CH1 and CH2.  
    def get_output_series(self):
        
        output_series = str(self.inst.query("OUTP:SER?"))
        return(output_series)
    
        #Sets the output state of all three channels. 
    def set_output_states(self, boolean):
        
        if str(boolean).upper() in ['ON', 'OFF']:
            self.inst.write(f"OUTP {boolean}.upper()")
        if int(boolean) in range(2):
            self.inst.write(f"OUTP {boolean}")
        else:
            raise ValueError("Value Error. Please enter ON, OFF, 0, or 1.")
        
        #Returns the output state of all three channels.  
    def get_output_states(self):
        
        output_states = str(self.inst.query("OUTP?"))
        return(output_states)
    
        #Sets the delay time for the output timer function.  
    def set_time_delay(self, NR2):
        
        if 0.1 <= float(NR2) <= 99999.9:
            self.inst.write(f"OUTP:TIM:DEL {NR2}")
        else:
            raise ValueError("Value Error. Please enter a value between 0.1 "
                             "and 99999.9.")
        
        #Returns the delay time for the output timer function.
    def get_time_delay(self):
        
        time_delay = str(self.inst.query("OUTP:TIM:DEL?"))
        return(time_delay)
    
        #Sets the output timer state for the presently selected channel.  
    def set_time_delay_channel(self, boolean):
        
        if str(boolean).upper() in ['ON', 'OFF']:
            self.inst.write(f"OUTP:TIM {boolean}.upper()")
        if int(boolean) in range(2):
            self.inst.write(f"OUTP:TIM {boolean}")
        else:
            raise ValueError("Value Error. Please enter ON, OFF, 0, or 1.")
        
        #Returns output timer state for presently selected channel.  
    def get_time_delay_channel(self):
        
        time_delay_channel = str(self.inst.query("OUTP:TIM?"))
        return(time_delay_channel)
    
        #Sets the value of the voltage step.   
    def set_volt_step(self, NR2, unit = 'V'):
        
        if str(unit).upper() == 'MV':
            NR2 = NR2 / 1000
        if str(unit).upper() == 'KV':
            NR2 = NR2 * 1000
        self.inst.write(f"VOLT:STEP {NR2}")
        
        #Returns value of the voltage step.  
    def get_volt_step(self):
        
        volt_step = str(self.inst.query("VOLT:STEP?"))
        return(volt_step)
    
        #Decreases the voltage value of the present channel by one step,
        #as specified by the set_volt_step command.  
    def volt_down(self):
        
        self.inst.write("VOLT:DOWN")
        
        #Increases the voltage value of the present channel by one step,
        #as specified by the set_volt_step command.  
    def volt_up(self):
        
        self.inst.write("VOLT:UP")
        
        #Sets the voltage value of the power supply.  
    def set_volt(self, NRf):
    
        if self.get_model == '30-3':
            if self.get_channel in ['CH1', 'CH2']:
                if 0 <= float(NRf) <= 30:
                    self.inst.write(f"VOLT {NRf}")
            elif self.get_channel == 'CH3':
                if 0 <= float(NRf) <= 5:
                    self.inst.write(f"VOLT {NRf}")
        if self.get_model == '30-6':
            if self.get_channel in ['CH1', 'CH2']:
                if 0 <= float(NRf) <= 30:
                    self.inst.write(f"VOLT {NRf}")
            elif self.get_channel == 'CH3':
                if 0 <= float(NRf) <= 5:
                    self.inst.write(f"VOLT {NRf}")
        if self.get_model == '60-3':
            if self.get_channel in ['CH1', 'CH2']:
                if 0 <= float(NRf) <= 60:
                    self.inst.write(f"VOLT {NRf}")
            elif self.get_channel == 'CH3':
                if 0 <= float(NRf) <= 5:
                    self.inst.write(f"VOLT {NRf}")       
        else:
            raise ValueError("Value Error. Please refer to the manual for "
                             "correct inputs.")
        
        #Returns the voltage value of the power supply.
    def get_volt_power(self):
        
        volt_power = str(self.inst.quert("VOLT?"))
        return(volt_power)
    
        #Sets the voltage limit for the present channel.  
    def set_volt_limit(self, NRf):
        
        if self.get_model == '30-3':
            if self.get_channel in ['CH1', 'CH2']:
                if 0 <= float(NRf) <= 30:
                    self.inst.write(f"VOLT:LIM {NRf}")
            elif self.get_channel == 'CH3':
                if 0 <= float(NRf) <= 5:
                    self.inst.write(f"VOLT:LIM {NRf}")
        if self.get_model == '30-6':
            if self.get_channel in ['CH1', 'CH2']:
                if 0<= float(NRf) <= 30:
                    self.inst.write(f"VOLT:LIM {NRf}")
            elif self.get_channel == 'CH3':
                if 0 <= float(NRf) <= 5:
                    self.inst.write(f"VOLT:LIM {NRf}")
        if self.get_model == '60-3':
            if self.get_channel in ['CH1', 'CH2']:
                if 0 <= float(NRf) <= 60:
                    self.inst.write(f"VOLT:LIM {NRf}")
            elif self.get_channel == 'CH3':
                if 0 <= float(NRf) <= 5:
                    self.inst.write(f"VOLT:LIM {NRf}")   
        else:
            raise ValueError("Value Error. Please refer to the manual for "
                             "correct inputs.")
        
        #Returns the voltage limit for the present channel.  
    def get_volt_limit(self):
        
        volt_limit = str(self.inst.query("VOLT:LIM?"))
        return(volt_limit)
    
        #Enables or disables the voltage limit function.  
    def volt_limit_stat(self, boolean):
        
        if str(boolean).upper() in ['ON', 'OFF']:
            self.inst.write(f"VOLT:LIM:STAT {boolean}.upper()")
        if int(boolean) in range(2):
            self.inst.write(f"VOLT:LIM:STAT {boolean}")
        else:
            raise ValueError("Value Error. Please enter 0, 1, ON, or OFF.")
        
        #Returns status of the voltage limit functions.  
    def get_limit_stat(self):
        
        limit_stat_volt = str(self.inst.query("VOLT:LIM:STAT?"))
        return(limit_stat_volt)
    
        #Reads the Operation Condition Register of the status model.  
    def get_ocr(self):
        
        ocr = str(self.inst.query("STAT:OPER:COND?"))
        return(ocr)
    
        #Sets the Operation Event Enable Register of the status model.  
    def set_oeer(self, NR1):
        
        if int(NR1) in range(256):
            self.inst.write(f"STAT:OPER:ENAB {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between 0 "
                             "and 255.")
     
        #Returns the Operation Event Enable Register of the status model.  
    def get_oeer(self):
        
        oeer = str(self.inst.query("STAT:OPER:ENAB?"))
        return(oeer)
    
        #Reads and then clears the Operation Event Register of 
        #the status model.  
    def get_oer(self):
        
        oer = str(self.inst.query("STAT:OPER?"))
        return(oer)
    
        #Sets the Operation Enable Register of the status model.  
    def set_enab(self, NR1):
        
        if int(NR1) in range(256):
            self.inst.write(f"STAT:OPER:INST:ENAB {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between 0 "
                             "and 255.")
        
        #Returns the Operation Enable Register of the status mode.
    def get_enab(self):
        
        enab_reg = str(self.inst.query("STAT:OPER:INST:ENAB?"))
        return(enab_reg)
    
        #Reads and then clears the Operation Instrument Event Register of
        #the status model. 
    def get_oier(self):
        
        oier = str(self.inst.query("STAT:OPER:INST?"))
        return(oier)
    
        #Returns the Operation Instrument Summary Condition Register
        #of the status model for the specified channel.  
    
    def get_oiscr(self, x):
        
        if int(x) in range(1, 4):
            oiscr = str(self.inst.query(f"STAT:OPER:INST:ISUM{x}:COND?"))
            return(oiscr)
        else:
            raise ValueError("Value Error. Please enter 1, 2, or 3.")
        
        #Sets the Operation Instrument Summary Enable Register of the status
        #model for the specified channel.  
    def set_oiser(self, x, NR1):
        
        if int(x) in range(1, 3) and int(NR1) in range(256):
            self.inst.write(f"STAR:OPER:INST:ISUM{x}:ENAB {NR1}")
        else:
            raise ValueError("Value Error. Please enter 1, 2, or 3 for x and "
                             "an integer between 0 and 255 for NR1.")
        
        #Returns the Operation Instrument Summary Enable Register of the status
        #model for the specified channel.  
    def get_oister(self, x):
        
        if int(x) in range(1, 4):
            oiser = str(self.inst.query(f"STAT:OPER:INST:ISUM{x}:ENAB?"))
            return(oiser)
        else:
            raise ValueError("Value Error. Please enter 1, 2, or 3.")
        
        #Returns the Operation Instrument Summary Event Register of the
        #status model for the specified channel.  
    def get_inst_event(self, x):
        
        if int(x) in range(1, 4):
            inst_event = str(self.inst.query(f"STAT:OPER:INST:ISUM{x}?"))
            return(inst_event)
        else:
            raise ValueError("Value Error. Please enter 1, 2, or 3.")
        
        #Resets all bits in the status model.  
    def reset_status(self):
        
        self.inst.write("STAT:PRES")
        
        #Returns the Questionable Condition Register of the status model.
        #If the value of the bit in the questionable condition register
        #changes, it will cause the corresponding bit in the Questionable
        #Event Register to be 1.  
    def get_qcr(self):
        
        qcr = str(self.inst.query("STAT:QUES:COND?"))
        return(qcr)
    
        #Sets the Questionable Event Enable Register (QENR) of the
        #status model. The QENR is an eight-bit mask register that determines
        #which bits in the Questionable Event Register should affect the state
        #of the QUES bit in the status byte register.  
    def set_qenr(self, NR1):
        
        if int(NR1) in range(256):
            self.inst.write(f"STAT:QUES:ENAB {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between 0 "
                             "and 255.")
        
        #Returns the Questionable Event Enable Register (QENR) of the
        #status model. The QENR is an eight-bit mask register that determines
        #which bits in the Questionable Event Register should affect the state
        #of the QUES bit in the status byte register.  
    def get_qenr(self):
        
        qenr = str(self.inst.query("STAT:QUES:ENAB?"))
        return(qenr)
    
        #Returns and resets the Questionable Event Register of the status
        #model.  
    def get_qer(self):
        
        qer = str(self.inst.query("STAT:QUES?"))
        return(qer)
    
        #Sets the Questionable Instrument Enable Register of the status 
        #model.  
    def set_qier(self, NR1):
        
        if int(NR1) in range(65536):
            self.inst.write(f"STAT:QUES:INST:ENAB {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between 0 "
                             "and 65,536.")
        
        #Returns the Questionable Instrument Enable Register of the status 
        #model.  
    def get_qier(self):
        
        qier = self.inst.query("STAT:QUES:INST:ENAB?")
        return(qier)
    
        #Returns and clears the Questionable Instrument Event Register of the
        #status model.  
    def get_qier_status(self):
        
        qier = self.inst.query("STAT:QUES:INST?")
        return(qier)
    
        #Returns the Questionable Instrument Summary Condition Register of the
        #status model for the specified channel.  
    def get_qier_channel(self, x):
        
        if x in range(1, 4):
            qier_channel = self.inst.query(f"STAT:QUES:INST:ISUM{x}:COND?")
            return(qier_channel)
        else:
            raise ValueError("Value Error. Please enter 1, 2, or 3.")
        
        #Sets the contents of the Questionable Instrument Summary Event
        #Enable Register of the status model for the specified channel.  
    def set_qiseer(self, x, NR1):
        
        if int(x) in range(1, 4) and int(NR1) in range(65536):
            self.inst.write(f"STAT:QUES:INST:ISUM{x}:ENAB {NR1}")
        else:
            raise ValueError("Value Error. Please enter 1, 2, or 3 for x and "
                             "an integer between 0 and 65,535 for NR1.")
        
        #Returns the contents of the Questionable Instrument Summary Event
        #Enable Register of the status model for the specified channel.  
    def get_qiseer(self, x):
        
        if int(x) in range(1, 4):
            qiseer = str(self.inst.query(f"STAT:QUES:INST:ISUM{x}:ENAB?"))
            return(qiseer)
        else:
            raise ValueError("Value Error. Please enter 1, 2, or 3.")
        
        #Returns the Operation Instrument Summary Event Register of the status
        #model for the specified channel.  
    def get_oiser_channel(self, x):
        
        if int(x) in range(1, 4):
            oiser_channel = str(self.inst.query(f"STAT:QUES:INST:ISUM{x}"))
            return(oiser_channel)
        else:
            raise ValueError("Value Error. Please enter 1, 2, or 3.")
        
        #Tests the beeper function of the power supply.
        #If it passes the test, a beep is issued.  
    def beep(self):
        
        self.inst.write("SYST:BEEP")
        
        #Retruns the GPIB address of the device.  
    def get_gpib(self):
        
        gpib = str(self.inst.query("SYST:COMM:GPIB:RDEV:ADDR?"))
        return(gpib)
    
        #Takes the instrument out of remote operation and restores the
        #operation of front-panel controls.  
    def get_error(self):
        
        error = str(self.inst.query("SYST:ERR?"))
        return(error)
    
        #Switches the power supply into control from the front panel.  
    def switch_local(self):
        
        self.inst.write("SYST:LOC")
        
        #Takes the instrument out of front-panel control mode and switches it
        #to remote control mode.  
    def remote_control(self):
        
        self.inst.write("SYST:REM")
        
        #Locks the power supply in remote control mode. When this command is
        #executed, pressing the LOCAL button does not switch the instrument to
        #local control mode.  
    def lock_power(self):
        
        self.inst.write("SYST:RWL")

        #Returns the SCPI version of the instrument.  
    def get_scpi(self):
        
        scpi = str(self.inst.query("SYST:VERS?"))
        return(scpi)
