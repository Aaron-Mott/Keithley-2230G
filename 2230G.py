# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 15:07:47 2020

@author: Aaron Mott
aaron.b.mott@gmail.com
"""


import visa

class KEI2230G():
    
    def __innit__(self, inst_address, baud_rate = 9600):
        """
        Initializes the instrument with instrument address, baud rate,
        termination characters, and timeout.

        Parameters
        ----------
        inst_address : str
            The port address of the instrument.
        baud_rate : int, optional
             The default is 9600, but may be set to 4800, 9600, 19200, 38400,
                                                    57600, or 115200.
        """
        
        self.rm = visa.ResourceManager()
        self.inst = self.rm.open_resource(self.instr_address,
                                          baud_rate,
                                          term_chars = '\n',
                                          timeout = None)
        
    def clear_status(self):
        """Clears all the event registers and error queue."""
        self.inst.write("*CLS")
        
    def set_eser(self, NR1):
        """
        Sets the Standard Event Enable Register.

        Parameters
        ----------
        NR1 : int
            A value from 0 through 255. The binary bits of the ESER are set
            according to this value.
        """
        if int(NR1) in range(256):
            self.inst.write(f"*ESE {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between "
                             "0 and 255.")
        
    def get_standard_event(self):
        """Reads the Standard Event Enable Register."""
        current_register = str(self.inst.query("*ESE?"))
        return(current_register)
        
    def get_standard_event_and_clear(self):
        """Reads the Standard Event Status Register and clears it."""
        current_register = str(self.inst.query("*ESR?"))
        return(current_register)
        
    def get_info(self):
        """
        Returns the instrument manufacturer, model, serial number, and firmware
        revision level.
        """
        info = str(self.inst.query("*IDN?")).split(',')
        return(" Manufacturer: " + info[0] + '\n',
              "Model: " + info[1] + '\n',
              "Serial Number: " + info[2]+'\n',
              " Firmware Version: " + info[3])
    
    def get_model(self):
        """Returns model type (30-3, 30-6, or 60-3)."""
        model = (str(self.get_info.split('\n')[1].split(":")
                     [1].replace(" ", ""))[6:10])
        return(model)
        
    def set_op_complete(self):
        """
        Set the Operation Complete bit in the Standard Event Status Register
        #to 1 after all pending commands have been executed.
        """
        self.inst.write("*OPC")
        
    def get_op_complete(self):
        """Indicates whether all pending OPC operations are finished."""
        op = self.inst.query("*OPC?")
        if int(op) == 1:
            return("All OPC operations are finished.")
        else:
            return("Some OPC operations are still ongoing.")
            
    def set_psc(self, NR1):
        """
        This command specifies sets the power status clear flag to true
        or false. 0 is false and 1 is true.

        Parameters
        ----------
        NR1 : int
            Either 0 or 1.

        Raises
        ------
        ValueError
            DESCRIPTION.

        Returns
        -------
        None.
        """
        if int(NR1) in range(2):
            self.inst.write(f"*PSC {NR1}")
        else:
            raise ValueError("Value Error. Please enter 0 for false or 1 for "
                             "true.")
        
    def set_setup(self, NR1):
        """
        Recalls the setups you saved in the specified memory location.
        Parameters
        ----------
        NR1 : int
            An integer value from 1 to 36 that specifies the location of setup
            memory.
        """
        if int(NR1) in range(1, 37):
            self.inst.write(f"*RCL {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between 1 "
                             "and 36.")
            
    def reset_settings(self):
        """Resets the power supply to default settings."""
        self.inst.write("*RST")
        
    def save_to(self, NR1):
        """
        Saves the present current, voltage, and maximum voltage settings
        of the power supply into specified memory.

        Parameters
        ----------
        NR1 : int
            An integer value from 1 to 36.
        """
        if int(NR1) in range(1, 37):
            self.inst.write(f"*SAV {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between 1 "
                             "and 36.")
        
    def set_status_byte(self, NR1):
        """
        Sets or the bits in the Status Byte Enable Register.

        Parameters
        ----------
        NR1 : int
            An integer value 0 to 255. The binary bits of the Status Request
            Enable Register (SRER) are set according to this value. Using an
            out-of-range value causes an execution error.

        """
        if int(NR1) in range(256):
            self.inst.write(f"*SRE {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between 0 "
                             "and 255.")
        
    def get_status_byte(self):
        """Returns Status Byte Enable Register."""
        status_byte = str(self.inst.query("*SRE"))
        return(status_byte)
    
    def get_sbr(self):
        """Reads the data in the Status Byte Register."""
        sbr = str(self.inst.query("*STB"))
        return(sbr)
    
    def self_test(self):
        """Initiates a self-test and reports any errors."""
        error_code = str(self.inst.query("*TST"))
        return(error_code)
    
    def wait(self):
        """
        Prevents the instrument from executing further commands or queries
        until all pending commands are complete.
        """
        self.inst.write("*WAI")
    
    def cal_cle(self):
        """Clears the calibration information on the instrument."""
        self.inst.write("CAL:CLE")
        
    def cal_curr(self, NR2):
        """
        Sets the actual output current value of the calibration point.

        Parameters
        ----------
        NR2 : float
            Current value of the calibration point.
        """
        self.inst.write(f"CAL:CURR {NR2}")
        
    def cal_curr_lev(self, point):
        """
        Sets the current calibration points.

        Parameters
        ----------
        point : str
            Points P1 and P2 must be calibrated in numeric order..
        """
        if str(point).upper() == 'P1' or 'P2':
            self.inst.write(f"CAL:CURR:LEV {point}.upper()")
        else:
            raise ValueError("Value Error. Please enter P1 or P2.")
        
    def cal_init(self):
        """Sets the current calibration coefficient as the default value."""
        self.inst.write("CAL:INIT")
        
    def cal_sav(self):
        """Saves the calibration coefficient into nonvolatile memory."""
        self.inst.write("CAL:SAV")
        
    def cal_sec(self, boolean, password):
        """
        Enables or disables calibration mode.

        Parameters
        ----------
        boolean : int
            0 enables the calibration mode, 1 disables calibration mode.
        password : int
            The password is the model number of the power supply..
        """
        #Gets serial number.
        code = str(self.get_info.split('\n')[1].split(":")[1].replace(" ", ""))
        #Checks if state and password are correct.
        if boolean in range(2) and str(password) == code:
            self.inst.write(f"CAL:SEC {boolean} {password}")
        else:
            raise ValueError("Value Error. Please refer to the manual for "
                             "correct inputs.")
        
    def cal_sec_unsecure(self, boolean):
        """
        Enables or disables calibration mode without asking for password.

        Parameters
        ----------
        boolean : int
            0 enables the calibration mode, 1 disables calibration mode.
        """
        code = str(self.get_info.split('\n')[1].split(":")[1].replace(" ", ""))
        if boolean in range(2):
            self.inst.write(f"CAL:SEC {boolean} {code}")
        else:
            raise ValueError("Value Error. Please enter 0 or 1.")
            
    def cal_str(self, string):
        """
        Writes the calibration information of the instrument.

        Parameters
        ----------
        string : str
            The maximum length of the string is 22 bytes.
        """
        if 0 <= len(str(string).encode('utf8')) <= 22:
            self.inst.write(f"CAL:STR {string}")
        else:
            raise ValueError("Value Error. Please enter a string no more than "
                             "22 bytes.")
            
    def get_cal(self):
        """Returns calibration information of the intrsument."""
        cal = str(self.inst.query("CAL:STR?"))
        return(cal)
    
    def cal_volt(self, NR2):
        """
        Sets the actual output voltage value of the calibration point.

        Parameters
        ----------
        NR2 : float
            The voltage value of the calibration point.
        """
        if 0 <= float(NR2) <= 30:
            self.inst.write(f"CAL:VOLT {NR2}")
        else:
            raise ValueError("Value Error. Please refer to the manual for "
                             "correct inputs.")
        
    def cal_volt_lev(self, point):
        """
        Sets the voltage calibration points. The second if statement is if the
        user only enters the number and is checked as an integer instead of a
        string to help differentiate between entering the command with or
        without "P" trailing the point.

        Parameters
        ----------
        point : str, int
            Points P1, P2, P3, and P4 must be calibrated in numeric order.
        """
        if str(point).upper() in ['P1', 'P2', 'P3', 'P4']:
            self.inst.write(f"CAL:VOLT:LEV {point}.upper()")
        if int(point) in range(1, 5):
            self.inst.write(f"CAL:VOLT:LEV P{point}")
        else:
            raise ValueError("Value Error. Please enter P1, P2, P3, or P4.")
        
    def inst_com(self):
        """Returns connection state of the channels."""
        comb = str(self.inst.query("INST:COMB?"))
        return(comb)
    
    def inst_comb_off(self):
        """Turns off the connection of channels."""
        self.inst.write("INST:COM:OFF")
        
    def set_parallel(self, level):
        """
        Specifies that the instrument combines the present readings of 
        channels when they are connected in parallel. The two last if
        statements are if the user only enters numbers and are checked as
        integers instead of a string to help differentiate between entering
        the command with or without "CH" trailing the channel number.

        Parameters
        ----------
        level : str, int
             Channels to be combined in parallel.
        """
        if str(level).upper() in ["CH1CH2", "CH2CH3", "CH1CH2CH3"]:
            self.inst.write(f"INST:COMB:PAR {level}.upper()")
        if int(level) in [12, 23]:
            self.inst.write(f"INST:COMB:PAR CH{str(level)[0]}"
                                            "CH{str(level)[1]}")
        if int(level) == 123:
            self.inst.write(f"INST:COMB:PAR CH1CH2CH3")
        else:
            raise ValueError("Value Error. Please enter CH1CH2, CH2CH3, or "
                             "CH1CH2CH3.")
        
    def inst_com_ser(self):
        """
        Combines the present voltage readings on channel 1 (CH1) and
        channel 2 (CH2) when they are connected in series.
        """
        self.inst.write("INST:COMB:SER")
        
    def set_track(self, level):
        """
        Sets channels to tracking mode. The two last if statesments
        are if the user only enters numbers and are checked as integers
        instead of a string to help differentiate between entering the
        command with or without "CH" trailing the channel number.

        Parameters
        ----------
        level : str
            The channels to be set to tracking mode.

        """
        if str(level).upper() in ['CH1CH2', 'CH2CH3', 'CH1CH2CH3']:
            self.inst.write(f"INST:COMB:TRAC {level}.upper()")
        if int(level) in [12, 23]:
            self.inst.write(f"INST:COMB:TRAC CH{str(level)[0]}"
                                            "CH{str(level)[1]")
        if int(level) == 123:
            self.inst.write(f"INST:COMB:TRAC CH1CH2CH3")
        else:
            raise ValueError("Value Error. Please enter CH1CH2, CH2CH3, or "
                             "CH1CH2CH3.")
        
    def select_channel(self, NR1):
        """
        Selects channel number.

        Parameters
        ----------
        NR1 : int
            The channel number.

        """
        if int(NR1) in range(1, 4):
            self.inst.write(f"INST:NSEL {NR1}")
        else:
            raise ValueError("Value Error. Please enter 1, 2, or 3.")
        
    def set_channel(self, level):
        """
        Selects the channel.

        Parameters
        ----------
        level : str
            The channel.
        """
        if str(level).upper() in ["CH1", "CH2", "CH3"]:
            self.inst.write(f"INST {level}.upper()")
        if int(level) in range(1, 4):
            self.inst.write(f"INST CH{level}")
        else:
            raise ValueError("Value Error. Please enter CH1, CH2, or CH3.")
        
    def get_channel(self):
        """Queries selected channel."""
        channel = str(self.inst.query("INST?"))
        return(channel)
    
    def get_channel_curr(self, level):
        """
        Queries the current reading on the specified channel.

        Parameters
        ----------
        level : str, int
            The selected channel or channels with the current readings to
            return.
        """
        if str(level).upper() in ["CH1", "CH2", "CH3", "ALL"]:
            reading = str(self.inst.query(f"FETC:CURR? {level}.upper()"))
            return(reading)
        if int(level) in range(1, 4):
            reading = str(self.inst.query(f"FETC:CURR? CH{level}"))
            return(reading)
        if int(level) == 123:
            reading = str(self.inst.query(f"FETC:CURR? ALL"))
            return(reading)
        else:
            raise ValueError("Value Error. Please enter CH1, CH2, CH3, or "
                             "ALL.")
        
    def get_power(self, level):
        """
        Queries the present power measurement on a specified channel or
        channels.

        Parameters
        ----------
        level : str, int
            The channel or channels with the measurement to return.
        """
        if str(level).upper() in ["CH1", "CH2", "CH3", "ALL"]:
            power = str(self.inst.query(f"FETC:POW? {level}.upper()"))
            return(power)
        if int(level) in range(1, 4):
            power = str(self.inst.query(f"FETC:POW? CH{level}"))
            return(power)
        if int(level) == 123:
            power = str(self.inst.query(f"FETC:POW? ALL"))
            return(power)
        else:
            raise ValueError("Value error. Please enter CH1, CH2, CH3, or "
                             "ALL.")
        
    def get_volt(self, level):
        """
        Returns new current voltage on a specified channel or channels.
        """
        if str(level).upper() in ["CH1", "CH2", "CH3", "ALL"]:
            volt = str(self.inst.query(f"FETC:VOLT? {level}.upper()"))
            return(volt)
        else:
            raise ValueError("Value Error. Please enter CH1, CH2, CH3, or "
                             "ALL.")
        
    def meas_curr(self, level): 
        """
        Initiates and executes a new current measurement or queries the
        new measured current on a specified channel or channels.

        Parameters
        ----------
        level : str, int
            The channel or channels on which to make a new current measurement.
        """
        if str(level).upper() in ["CH1", "CH2", "CH3", "ALL"]:
            curr_meas = str(self.inst.query(f"MEAS:CURR? {level}.upper()"))
            return(curr_meas)
        if int(level) in range(1, 4):
            curr_meas = str(self.inst.query(f"MEAS:CURR? CH{level}"))
            return(curr_meas)
        if int(level) == 123:
            curr_meas = str(self.inst.query(f"MEAS:CURR? ALL"))
            return(curr_meas)
        else:
            raise ValueError("Value Error. Please enter CH1, CH2, CH3, or "
                             "ALL.")
    
    def meas_power(self, level):
        """
        Initiates and executes a new power measurement or queries the new
        measured power.

        Parameters
        ----------
        level : int
            The channel or channels on which to make a new power measurement.
        """
        if str(level).upper() in ["CH1", "CH2", "CH3", "ALL"]:
            pow_meas = str(self.inst.query(f"MEAS:POW? {level}.upper()"))
            return(pow_meas)
        if int(level) in range(1, 4):
            pow_meas = str(self.inst.query(f"MEAS:POW? CH{level}"))
            return(pow_meas)
        if int(level) == 123:
            pow_meas = str(self.inst.query(f"MEAS:POW? ALL"))
            return(pow_meas)
        else:
            raise ValueError("Value Error. Please enter CH1, CH2, CH3, or "
                             "ALL.")
        
    def meas_volt(self, level):
        """
        Initiates and executes a new voltage measurement or queries the new
        measured voltage.

        Parameters
        ----------
        level : int, str
            The channel or channels on which to make a new voltage measurement.
        """
        if str(level).upper() in ["CH1", "CH2", "CH3", "ALL"]:
            volt_meas = str(self.inst.query(f"MEAS:VOLT? {level}.upper()"))
            return(volt_meas)
        if int(level) in range(1, 4):
            volt_meas = str(self.inst.query(f"MEAS:VOLT? CH{level}"))
            return(volt_meas)
        if int(level) == 123:
            volt_meas = str(self.inst.query(f"MEAS:VOLT? ALL"))
            return(volt_meas)
        else:
            raise ValueError("Value Error. Please enter CH1, CH2, CH3, or "
                             "ALL.")
        
    def apply_volt(self, level, volt, curr):
        """
        Sets voltage and current levels on a specified channel with a single
        command message.

        Parameters
        ----------
        level : int, str
            The channel to apply the settings to.
        volt : int, str
            The voltage value to apply.
        curr : int, str
            The current value to apply.
        """
        if self.get_model == '30-3':
            if str(level.upper()) in ["CH1", "CH2"]:
                if (str(volt).upper() and str(curr).upper() in 
                    ["MAX", "MIN", "DEF", "UP", "DOWN"] or
                        0 <= float(volt) <= 31 and 0 <= float(curr) <= 4):
                        self.inst.write((f"APPL {level}.upper(), {volt}.upper,"
                                         "{curr}.upper()"))
            if int(level) in range(1, 3):
                if (str(volt).upper() and str(curr).upper() in 
                    ["MAX", "MIN", "DEF", "UP", "DOWN"] or
                        0 <= float(volt) <= 31 and 0 <= float(curr) <= 4):
                        self.inst.write((f"APPL CH{level}, {volt}.upper,"
                                         "{curr}.upper()"))
            if str(level.upper()) == 'CH3':
                if (str(volt).upper() and str(curr).upper() in 
                    ["MAX", "MIN", "DEF", "UP", "DOWN"] or
                    0 <= float(volt) in 0 <= 5 and 0 <= float(curr) <= 3):
                        self.inst.write((f"APPL {level}.upper(), {volt}.upper," 
                                         "{curr}.upper()"))
            if int(level) == 3:
                if (str(volt).upper() and str(curr).upper() in 
                    ["MAX", "MIN", "DEF", "UP", "DOWN"] or
                    0 <= float(volt) in 0 <= 5 and 0 <= float(curr) <= 3):
                        self.inst.write((f"APPL CH{level}, {volt}.upper," 
                                         "{curr}.upper()"))
        if self.get_model == '30-6':
            if str(level.upper()) in ["CH1", "CH2"]:
                if (str(volt).upper() and str(curr).upper() in 
                    ["MAX", "MIN", "DEF", "UP", "DOWN"] or
                    0 <= float(volt) <= 30 and 0 <= float(curr) <= 6):
                        self.inst.write((f"APPL {level}.upper(), {volt}.upper," 
                                         "{curr}.upper()"))
            if int(level) in range(1, 3):
                if (str(volt).upper() and str(curr).upper() in 
                    ["MAX", "MIN", "DEF", "UP", "DOWN"] or
                    0 <= float(volt) <= 30 and 0 <= float(curr) <= 6):
                        self.inst.write((f"APPL CH{level}, {volt}.upper," 
                                         "{curr}.upper()"))
            if str(level.upper()) == 'CH3':
                if (str(volt).upper() and str(curr).upper() in 
                    ["MAX", "MIN", "DEF", "UP", "DOWN"] or
                    0 <= float(volt) <= 5 and 0 <= float(curr) <= 3):
                        self.inst.write((f"APPL {level}.upper(), {volt}.upper," 
                                         "{curr}.upper()"))
            if int(level) == 3:
                if (str(volt).upper() and str(curr).upper() in 
                    ["MAX", "MIN", "DEF", "UP", "DOWN"] or
                    0 <= float(volt) <= 5 and 0 <= float(curr) <= 3):
                        self.inst.write((f"APPL CH{level}, {volt}.upper," 
                                         "{curr}.upper()"))
        if self.get_model == '60-3':
            if str(level.upper()) in ["CH1", "CH2"]:
                if (str(volt).upper() and str(curr).upper() in 
                    ["MAX", "MIN", "DEF", "UP", "DOWN"] or
                    0 <= float(volt) <= 60 and 0 <= float(curr) <= 3):
                        self.inst.write((f"APPL {level}.upper(), {volt}.upper," 
                                         "{curr}.upper()"))
            if int(level) in range(1, 3):
                if (str(volt).upper() and str(curr).upper() in 
                    ["MAX", "MIN", "DEF", "UP", "DOWN"] or
                    0 <= float(volt) <= 60 and 0 <= float(curr) <= 3):
                        self.inst.write((f"APPL CH{level}, {volt}.upper," 
                                         "{curr}.upper()"))
            if str(level.upper()) == 'CH3':
                if (str(volt).upper() and str(curr).upper() in 
                    ["MAX", "MIN", "DEF", "UP", "DOWN"] or
                    0 <= float(volt) <= 5 and 0 <= float(curr) <= 3):
                        self.inst.write((f"APPL {level}.upper(), {volt}.upper," 
                                         "{curr}.upper()"))
            if int(level) == 3:
                if (str(volt).upper() and str(curr).upper() in 
                    ["MAX", "MIN", "DEF", "UP", "DOWN"] or
                    0 <= float(volt) <= 5 and 0 <= float(curr) <= 3):
                        self.inst.write((f"APPL CH{level}, {volt}.upper," 
                                         "{curr}.upper()"))
        else:
            raise ValueError("Value Error. Please refer to the manual for "
                             "correct inputs.")
        
    def set_output(self, boolean):
        """
        Sets the output state of the presently selected channel.

        Parameters
        ----------
        boolean : bool
            The output state.
        """
        if str(boolean).upper() in ["ON", "OFF"]:
            self.inst.write(f"CHAN:OUTP {boolean}.upper()")
        if int(boolean) in range(2):
            self.inst.write(f"CHAN:OUTP {boolean}.upper()")
        else:
            raise ValueError("Value Error. Please enter ON, OFF, 0, or 1.")
        
    def get_output(self):
        """Returns the output state of the presently selected channel."""
        channel_output = str(self.inst.query("CHAN:OUTP?"))
        return(channel_output)
    
    def set_curr_step(self, step, unit = 'A'):
        """
        Sets the amount to increase current level.

        Parameters
        ----------
        step : float
            The amount to increase the current.
        unit : str
            Unit of measure for the specified current value.
        """
        if str(unit).upper() == 'MA':
            step = step / 1000
        self.inst.write(f"CURR:STEP {step}A")
        
    def get_curr_step(self):
        """Returns the current step amount."""
        curr_step = str(self.inst.query("CURR:STEP?"))
        return(curr_step)
    
    def curr_down(self):
        """
        Decreases the current value of the present channel by one step.,
        as specified by the set_curr_step command.
        """
        self.inst.write("CURR:DOWN")
        
    def curr_up(self):
        """
        Increases the current value of the present channel by one step,
        as specified by the set_curr_step command.
        """
        self.inst.write("CURR:UP")
        
    def set_curr(self, NRf, unit = 'A'):
        """
        Sets the current value of the power supply.

        Parameters
        ----------
        curr : int, str
            The current value.
        unit : str
            Unit of measure (amperes).
        """
        if str(unit).upper() == 'MA':
            NRf = NRf / 1000
        if self.get_model == '30-3':
                if str(NRf).upper in ['MIN TO MAX', 'MIN', 'MAX', 'UP',
                                       'DOWN', 'DEF'] or 0 <= float(NRf) <= 3:
                    self.inst.write(f"CURR {NRf}")
        if self.get_model == '30-6':
            if self.get_channel in ['CH1', 'CH2']:
                if str(NRf).upper in ['MIN TO MAX', 'MIN', 'MAX', 'UP',
                                       'DOWN', 'DEF'] or 0 <= float(NRf) <= 6:
                    self.inst.write(f"CURR {NRf}")
            if self.get_channel == 'CH3':
                if str(NRf).upper in ['MIN TO MAX', 'MIN', 'MAX', 'UP',
                                       'DOWN', 'DEF'] or 0 <= float(NRf) <= 4:
                    self.inst.write(f"CURR {NRf}")
        if self.get_model == '60-3':
            if str(NRf).upper in ['MIN TO MAX', 'MIN', 'MAX', 'UP',
                                       'DOWN', 'DEF'] or 0 <= float(NRf) <= 3:
                self.inst.write(f"CURR {NRf}")
        else:
            raise ValueError("Value Error. Please refer to the manual for "
                             "correct inputs.")
        
    def get_curr(self):
        """Returns the current value of the power supply."""
        curr = str(self.inst.query("CURR?"))
        return(curr)
        
    def set_output_state(self, boolean):
        """
        Sets the output state of the power supply.

        Parameters
        ----------
        boolean : bool
            The output state of the power supply.
        """
        if str(boolean).upper() in ['ON', 'OFF']:
            self.inst.write(f"OUTP:ENAB {boolean}.upper()")
        if int(boolean) in range(2):
            self.inst.write(f"OUTP:ENAB {boolean}")
        else:
            raise ValueError("Value Error. Please enter ON, OFF, 0, or 1.")
        
    def set_output_parrallel(self, channels):
        """
        Sets the parallel synchronization state of the three channels.

        Parameters
        ----------
        channels : int, str
            The channel that the parallel synchronization state is applied to.
        """
        if str(channels).upper() in ['CH1CH2', 'CH2CH3', 'CH1CH2CH3']:
            self.inst.write(f"OUTP:PAR {channels}.upper()")
        if int(channels) in [12, 23]:
            self.inst.write(f"OUTP:PAR CH{str(channels)[0]}"
                                      "CH{str(channels)[1]}")
        if int(channels) == 123:
            self.inst.write("OUTP:PAR CH1CH2CH3")
        else:
            raise ValueError("Value Error. Please enter CH1CH2, CH2CH3, or "
                             "CH1CH2CH3.")
        
    def get_output_parrallel(self):
        """Returns the parallel synchronization state of the three channels."""
        output_parrallel = str(self.inst.query("OUTP:PAR?"))
        return(output_parrallel)
    
    def clear_state(self):
        """Clears the protection state of the power supply."""
        self.inst.write("OUTP:PROT:CLE")
        
    def set_output_series(self, boolean):
        """
        Sets the series synchronization state of channel 1 (CH1)
        and channel 2 (CH2). If channel 3 (CH3) and CH1 or CH3 and CH2 are
        in parallel synchronization states, an error is generated after
        the command is executed.

        Parameters
        ----------
        boolean : int, str
            The series synchronization state.
        """
        if str(boolean).upper() in ['ON', 'OFF']:
            self.inst.write(f"OUTP:SER {boolean}.upper()")
        if int(boolean) in range(2):
            self.inst.write(f"OUTP:SER {boolean}")
        else:
            raise ValueError("Value Error. Please enter ON, OFF, 0, or 1.")
        
    def get_output_series(self):
        """Returns the synchronization state of CH1 and CH2."""
        output_series = str(self.inst.query("OUTP:SER?"))
        return(output_series)
    
    def set_output_states(self, boolean):
        """
        Sets the output state of all three channels.

        Parameters
        ----------
        boolean : int, str
            The output state.
        """
        if str(boolean).upper() in ['ON', 'OFF']:
            self.inst.write(f"OUTP {boolean}.upper()")
        if int(boolean) in range(2):
            self.inst.write(f"OUTP {boolean}")
        else:
            raise ValueError("Value Error. Please enter ON, OFF, 0, or 1.")
        
    def get_output_states(self):
        """Returns the output state of all three channels."""
        output_states = str(self.inst.query("OUTP?"))
        return(output_states)
    
    def set_time_delay(self, NR2, unit = 'S'):
        """
        Sets the delay time for the output timer function.

        Parameters
        ----------
        NR2 : float
            The delay time.
        unit : str, optional
            Unit of measure for the delay time.
        """
        if str(unit).upper() == 'MS':
            NR2 = NR2 / 1000
        if 0.1 <= float(NR2) <= 99999.9:
            self.inst.write(f"OUTP:TIM:DEL {NR2}")
        else:
            raise ValueError("Value Error. Please enter a value between 0.1 "
                             "and 99999.9.")
        
    def get_time_delay(self):
        """Returns the delay time for the output timer function."""
        time_delay = str(self.inst.query("OUTP:TIM:DEL?"))
        return(time_delay)
    
    def set_time_delay_channel(self, boolean):
        """
        Sets the output timer state for the presently selected channel.

        Parameters
        ----------
        boolean : str, int
            The output timer state.
        """
        if str(boolean).upper() in ['ON', 'OFF']:
            self.inst.write(f"OUTP:TIM {boolean}.upper()")
        if int(boolean) in range(2):
            self.inst.write(f"OUTP:TIM {boolean}")
        else:
            raise ValueError("Value Error. Please enter ON, OFF, 0, or 1.")
        
    def get_time_delay_channel(self):
        """Returns output timer state for presently selected channel."""
        time_delay_channel = str(self.inst.query("OUTP:TIM?"))
        return(time_delay_channel)
    
    def set_volt_step(self, NR2, unit = 'V'):
        """
        Sets the value of the voltage step.

        Parameters
        ----------
        NR2 : int
            The value of the voltage step.
        unit : str, optional
            Unit of measure for the voltage step.
        """
        if str(unit).upper() == 'MV':
            NR2 = NR2 / 1000
        if str(unit).upper() == 'KV':
            NR2 = NR2 * 1000
        self.inst.write(f"VOLT:STEP {NR2}")
        
    def get_volt_step(self):
        """Returns value of the voltage step."""
        volt_step = str(self.inst.query("VOLT:STEP?"))
        return(volt_step)
    
    def volt_down(self):
        """
        Decreases the voltage value of the present channel by one step,
        as specified by the set_volt_step command.
        """
        self.inst.write("VOLT:DOWN")
        
    def volt_up(self):
        """
        Increases the voltage value of the present channel by one step,
        #as specified by the set_volt_step command.
        """
        self.inst.write("VOLT:UP")
        
    def set_volt(self, NRf, unit = 'V'):
        """
        Sets the voltage value of the power supply.

        Parameters
        ----------
        NRf : str, int
            The voltage value.
        unit: str, optional
            Sets the voltage value of the power supply.  
        """
        if self.get_model == '30-3':
            if self.get_channel in ['CH1', 'CH2']:
                if (str(NRf).upper() in ['MIN TO MAX', 'MIN', 'MAX', 'UP', 
                                        'DOWN', 'DEF'] or 
                                        0 <= float(NRf) <= 30):
                    self.inst.write(f"VOLT {NRf}.upper()")
            if self.get_channel == 'CH3':
                if str(NRf).upper() in ['MIN TO MAX', 'MIN', 'MAX', 'UP',
                                        'DOWN', 'DEF'] or 0 <= float(NRf) <= 5:
                    self.inst.write(f"VOLT {NRf}.upper()")
        if self.get_model == '30-6':
            if self.get_channel in ['CH1', 'CH2']:
                if (str(NRf).upper() in ['MIN TO MAX', 'MIN', 'MAX', 'UP',
                                        'DOWN', 'DEF'] or 
                                        0 <= float(NRf) <= 30):
                    self.inst.write(f"VOLT {NRf}.upper()")
            if self.get_channel == 'CH3':
                if (str(NRf).upper() in ['MIN TO MAX', 'MIN', 'MAX', 'UP',
                                        'DOWN', 'DEF'] or 
                                        0 <= float(NRf) <= 5):
                    self.inst.write(f"VOLT {NRf}.upper()")
        if self.get_model == '60-3':
            if self.get_channel in ['CH1', 'CH2']:
                if (str(NRf).upper() in ['MIN TO MAX', 'MIN', 'MAX', 'UP',
                                        'DOWN', 'DEF'] or 
                                        0 <= float(NRf) <= 60):
                    self.inst.write(f"VOLT {NRf}.upper()")
            if self.get_channel == 'CH3':
                if str(NRf).upper() in ['MIN TO MAX', 'MIN', 'MAX', 'UP',
                                        'DOWN', 'DEF'] or 0 <= float(NRf) <= 5:
                    self.inst.write(f"VOLT {NRf}.upper()")       
        else:
            raise ValueError("Value Error. Please refer to the manual for "
                             "correct inputs.")
        
    def get_volt_power(self):
        """Returns the voltage value of the power supply."""
        volt_power = str(self.inst.quert("VOLT?"))
        return(volt_power)
    
    def set_volt_limit(self, NRf):
        """
        Sets the voltage limit for the present channel.

        Parameters
        ----------
        NRf : str, int
            The voltage limit, 0 to the maximum rated voltage.
        """
        if self.get_model == '30-3':
            if self.get_channel in ['CH1', 'CH2']:
                if (str(NRf).upper() in ['MIN', 'MAX', 'DEF'] or
                    0 <= float(NRf) <= 30):
                        self.inst.write(f"VOLT:LIM {NRf}.upper()")
            if self.get_channel == 'CH3':
                if (str(NRf).upper() in ['MIN', 'MAX', 'DEF'] or
                    0 <= float(NRf) <= 5):
                        self.inst.write(f"VOLT:LIM {NRf}.upper()")
        if self.get_model == '30-6':
            if self.get_channel in ['CH1', 'CH2']:
                if (str(NRf).upper() in ['MIN', 'MAX', 'DEF'] or 
                    0 <= float(NRf) <= 30):
                        self.inst.write(f"VOLT:LIM {NRf}.upper()")
            if self.get_channel == 'CH3':
                if (str(NRf).upper() in ['MIN', 'MAX', 'DEF'] or
                    0 <= float(NRf) <= 5):
                        self.inst.write(f"VOLT:LIM {NRf}.upper()")
        if self.get_model == '60-3':
            if self.get_channel in ['CH1', 'CH2']:
                if (str(NRf).upper() in ['MIN', 'MAX', 'DEF'] or
                    0 <= float(NRf) <= 60):
                        self.inst.write(f"VOLT:LIM {NRf}.upper()")
            if self.get_channel == 'CH3':
                if (str(NRf).upper() in ['MIN', 'MAX', 'DEF'] or
                    0 <= float(NRf) <= 5):
                        self.inst.write(f"VOLT:LIM {NRf}.upper()")   
        else:
            raise ValueError("Value Error. Please refer to the manual for "
                             "correct inputs.")
        
    def get_volt_limit(self):
        """Returns the voltage limit for the present channel."""
        volt_limit = str(self.inst.query("VOLT:LIM?"))
        return(volt_limit)
    
    def volt_limit_stat(self, boolean):
        """
        Enables or disables the voltage limit function.

        Parameters
        ----------
        boolean : str, int
            The state of the voltage limit function.
        """
        if str(boolean).upper() in ['ON', 'OFF']:
            self.inst.write(f"VOLT:LIM:STAT {boolean}.upper()")
        if int(boolean) in range(2):
            self.inst.write(f"VOLT:LIM:STAT {boolean}")
        else:
            raise ValueError("Value Error. Please enter 0, 1, ON, or OFF.")
        
    def get_limit_stat(self):
        """Returns status of the voltage limit functions."""
        limit_stat_volt = str(self.inst.query("VOLT:LIM:STAT?"))
        return(limit_stat_volt)
    
    def get_ocr(self):
        """Reads the Operation Condition Register of the status model."""
        ocr = str(self.inst.query("STAT:OPER:COND?"))
        return(ocr)
    
    def set_oeer(self, NR1):
        """
        Sets the Operation Event Enable Register of the status model.

        Parameters
        ----------
        NR1 : int
            Operation Event Enable Register.
        """
        if int(NR1) in range(256):
            self.inst.write(f"STAT:OPER:ENAB {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between 0 "
                             "and 255.")
     
    def get_oeer(self):
        """Returns the Operation Event Enable Register of the status model."""
        oeer = str(self.inst.query("STAT:OPER:ENAB?"))
        return(oeer)
    
    def get_oer(self):
        """
        Reads and then clears the Operation Event Register of the status
        model. 
        """
        oer = str(self.inst.query("STAT:OPER?"))
        return(oer)
    
    def set_enab(self, NR1):
        """
        Sets the Operation Enable Register of the status model.

        Parameters
        ----------
        NR1 : int
             Operation Enable Register.
        """
        if int(NR1) in range(256):
            self.inst.write(f"STAT:OPER:INST:ENAB {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between 0 "
                             "and 255.")
        
    def get_enab(self):
        """Returns the Operation Enable Register of the status mode."""
        enab_reg = str(self.inst.query("STAT:OPER:INST:ENAB?"))
        return(enab_reg)
    
    def get_oier(self):
        """
        Reads and then clears the Operation Instrument Event Register of the
        status model.
        """
        oier = str(self.inst.query("STAT:OPER:INST?"))
        return(oier)
    
    def get_oiscr(self, x):
        """
        Returns the Operation Instrument Summary Condition Register
        #of the status model for the specified channel.

        Parameters
        ----------
        x : int
            Channel number.
        """
        if int(x) in range(1, 4):
            oiscr = str(self.inst.query(f"STAT:OPER:INST:ISUM{x}:COND?"))
            return(oiscr)
        else:
            raise ValueError("Value Error. Please enter 1, 2, or 3.")
        
    def set_oiser(self, x, NR1):
        """
        Sets the Operation Instrument Summary Enable Register of the status
        model for the specified channel.

        Parameters
        ----------
        x : int
            Channel number.
        NR1 : int
            Operation Instrument Summary Enable Register.
        """
        if int(x) in range(1, 3) and int(NR1) in range(256):
            self.inst.write(f"STAR:OPER:INST:ISUM{x}:ENAB {NR1}")
        else:
            raise ValueError("Value Error. Please enter 1, 2, or 3 for x and "
                             "an integer between 0 and 255 for NR1.")
        
    def get_oister(self, x):
        """
        Returns the Operation Instrument Summary Enable Register of the status
        model for the specified channel.

        Parameters
        ----------
        x : int
            Channel number.
        """
        if int(x) in range(1, 4):
            oiser = str(self.inst.query(f"STAT:OPER:INST:ISUM{x}:ENAB?"))
            return(oiser)
        else:
            raise ValueError("Value Error. Please enter 1, 2, or 3.")
        
    def get_inst_event(self, x):
        """
        Returns the Operation Instrument Summary Event Register of the
        #status model for the specified channel.

        Parameters
        ----------
        x : int
            Channel number.
        """
        if int(x) in range(1, 4):
            inst_event = str(self.inst.query(f"STAT:OPER:INST:ISUM{x}?"))
            return(inst_event)
        else:
            raise ValueError("Value Error. Please enter 1, 2, or 3.")
        
    def reset_status(self):
        """Resets all bits in the status model."""
        self.inst.write("STAT:PRES")
        
    def get_qcr(self):
        """
        Returns the Questionable Condition Register of the status model.
        If the value of the bit in the questionable condition register
        changes, it will cause the corresponding bit in the Questionable
        Event Register to be 1.
        """
        qcr = str(self.inst.query("STAT:QUES:COND?"))
        return(qcr)
    
    def set_qenr(self, NR1):
        """
        Sets the Questionable Event Enable Register (QENR) of the
        status model. The QENR is an eight-bit mask register that determines
        which bits in the Questionable Event Register should affect the state
        of the QUES bit in the status byte register.

        Parameters
        ----------
        NR1 : int
             Questionable Event Enable Register.
        """
        if int(NR1) in range(256):
            self.inst.write(f"STAT:QUES:ENAB {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between 0 "
                             "and 255.")
        
    def get_qenr(self):
        """
        Returns the Questionable Event Enable Register (QENR) of the
        status model. The QENR is an eight-bit mask register that determines
        which bits in the Questionable Event Register should affect the state
        of the QUES bit in the status byte register.
        """
        qenr = str(self.inst.query("STAT:QUES:ENAB?"))
        return(qenr)
    
    def get_qer(self):
        """
        Returns and resets the Questionable Event Register of the status
        model.
        """
        qer = str(self.inst.query("STAT:QUES?"))
        return(qer)
    
    def set_qier(self, NR1):
        """
        Sets the Questionable Instrument Enable Register of the status model.

        Parameters
        ----------
        NR1 : int
             Questionable Instrument Enable Register.
        """
        if int(NR1) in range(65536):
            self.inst.write(f"STAT:QUES:INST:ENAB {NR1}")
        else:
            raise ValueError("Value Error. Please enter an integer between 0 "
                             "and 65,536.")
        
    def get_qier(self):
        """
        Returns the Questionable Instrument Enable Register of the status
        model.
        """
        qier = self.inst.query("STAT:QUES:INST:ENAB?")
        return(qier)
    
    def get_qier_status(self):
        """
        Returns and clears the Questionable Instrument Event Register of the
        status model.
        """
        qier = self.inst.query("STAT:QUES:INST?")
        return(qier)
    
    def get_qier_channel(self, x):
        """
        Returns the Questionable Instrument Summary Condition Register of the
        status model for the specified channel.

        Parameters
        ----------
        x : int
            Channel number.
        """
        if x in range(1, 4):
            qier_channel = self.inst.query(f"STAT:QUES:INST:ISUM{x}:COND?")
            return(qier_channel)
        else:
            raise ValueError("Value Error. Please enter 1, 2, or 3.")
        
    def set_qiseer(self, x, NR1):
        """
        Sets the contents of the Questionable Instrument Summary Event
        Enable Register of the status model for the specified channel.

        Parameters
        ----------
        x : int
            Channel number.
        NR1 : int
            Questionable Instrument Summary Condition Register.
        """
        if int(x) in range(1, 4) and int(NR1) in range(65536):
            self.inst.write(f"STAT:QUES:INST:ISUM{x}:ENAB {NR1}")
        else:
            raise ValueError("Value Error. Please enter 1, 2, or 3 for x and "
                             "an integer between 0 and 65,535 for NR1.")
        
    def get_qiseer(self, x):
        """
        Returns the contents of the Questionable Instrument Summary Event
        Enable Register of the status model for the specified channel.

        Parameters
        ----------
        x : int
            Channel number.
        """
        if int(x) in range(1, 4):
            qiseer = str(self.inst.query(f"STAT:QUES:INST:ISUM{x}:ENAB?"))
            return(qiseer)
        else:
            raise ValueError("Value Error. Please enter 1, 2, or 3.")
        
    def get_oiser_channel(self, x):
        """
        Returns the Operation Instrument Summary Event Register of the status
        model for the specified channel.

        Parameters
        ----------
        x : int
            Channel numbers.
        """
        if int(x) in range(1, 4):
            oiser_channel = str(self.inst.query(f"STAT:QUES:INST:ISUM{x}"))
            return(oiser_channel)
        else:
            raise ValueError("Value Error. Please enter 1, 2, or 3.")
        
    def beep(self):
        """
        Tests the beeper function of the power supply. If it passes the test,
        a beep is issued.
        """
        self.inst.write("SYST:BEEP")
        
    def get_gpib(self):
        """Retruns the GPIB address of the device."""
        gpib = str(self.inst.query("SYST:COMM:GPIB:RDEV:ADDR?"))
        return(gpib)
    
    def get_error(self):
        """
        Takes the instrument out of remote operation and restores the
        operation of front-panel controls.
        """
        error = str(self.inst.query("SYST:ERR?"))
        return(error)
    
    def switch_local(self):
        """Switches the power supply into control from the front panel."""
        self.inst.write("SYST:LOC")
        
    def remote_control(self):
        """
        Takes the instrument out of front-panel control mode and switches it
        to remote control mode.
        """
        self.inst.write("SYST:REM")
        
    def lock_power(self):
        """
        Locks the power supply in remote control mode. When this command is
        executed, pressing the LOCAL button does not switch the instrument to
        local control mode.
        """
        self.inst.write("SYST:RWL")

    def get_scpi(self):
        """Returns the SCPI version of the instrument."""
        scpi = str(self.inst.query("SYST:VERS?"))
        return(scpi)
