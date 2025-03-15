# lab0x04 
# line sensor driver class
# Emily Nicoletta, Bea Loya
# 03/11/2025

# changed to calculate centroid with predefined weights

# import libraries/classes
from pyb import Pin, ADC

'''
# define line sensor channel pins
C0 = Pin.cpu.C0
B0 = Pin.cpu.B0
A4 = Pin.cpu.A4
C5 = Pin.cpu.C5
A7 = Pin.cpu.A7
B1 = Pin.cpu.B1
C4 = Pin.cpu.C4
C2 = Pin.cpu.C2

# put sensor pins in a list to be passed to LineSensor class
# line_sensor_pins = [C0, B0, A4, C5, A7, B1, C4, C2]
'''

class LineSensor:
    ''' line sensor driver class 
        functionalites:
            - reading sensor values and normalize raw sensor values from 0 to 1 
            - calibration for white surface
            - calibration for black surface
            - calculating centroid
    '''
    def __init__(self, sensor_pins, control_pin):
        ''' line sensor object instantiation
            inputs:
                - sensor_pins:
                    list of pin names where sensors channels are connected
                - control_pin
                    pin that controls brightness
            functionality:
                - defining pins as ADC
                - define control pin
                - set control pin high
                - define number of sensor based on how long the sensor list is
                - define the white values as 0
                - define the black values as 4095
                    assumes a 12 bit ADC
            outputs:
                - N/A
        '''
        # self attributes
        self.sensors = [ADC(Pin(pin)) for pin in sensor_pins]
        # define each pin in the sensor pin list as an ADC Pin
        self.ctrl = Pin(control_pin, mode = Pin.OUT_PP)
        # initialize control pin
        self.ctrl.high()
        # set control pin high
        self.num_sensors = len(sensor_pins)
        # define the number of sensors based on length of the sensor list
        self.white_values = [0] * self.num_sensors
        # initialize list for  white values (0 is basis)
        self.black_values = [4095] * self.num_sensors
        # initialize list for black values (4095 is basis - assume 12 bit ADC)

    def read_sensors(self):
        '''read_sensors method gets current sensor data
            inputs:
                - N/A
            functionality:
                - gets the raw sensor value of each sensor
                - normalize sensor data to 0 (white) to 1 (black) scale
            outputs:
                - normalized:
                    list of normalized sensor values
        '''
        self.ctrl.high()
        # set control pin high
        readings = [sensor.read() for sensor in self.sensors]
        # create list of sensor readings iterating thorugh each pin
        normalized = []
        # create empty list to append normalized values
        for i in range(self.num_sensors):
        # iterate though humber of sensors
            norm_value = ((readings[i] - self.white_values[i]) / 
                          (self.black_values[i] - self.white_values[i]))
            # find normalized value by comparing to calibrated white and black
            norm_value = max(0, min(1, norm_value))  
            # clamp values between 0 and 1
            normalized.append(norm_value)
            # append normalized value to list
        self.ctrl.low()
        return normalized
        # return list of normalized sensor data

    def calibrate_white(self, samples=100):
        '''calibrates the sensor array for a white surface
            inputs:
                - samples
                    value of desired samples
                    predefined as 100
            functionality:
                - allows user to set up and calibrate on white surface
                - averages the sensor reading values for a white surface  
                - updates self.white_values based on what sensors actually see
            outputs:
                - N/A
        '''
        print('place the sensor over a WHITE surface and press ENTER')
        # prompt user
        input()
        # wait for user confirmation
        print('calibrating white values...')
        # tell user calibration has started
        avg_readings = [0] * self.num_sensors
        # create list for number of sensors
        for _ in range(samples):
        # iterate for the number of specified samples
            readings = [sensor.read() for sensor in self.sensors]
            # read sensor data while on a white surface
            avg_readings = [avg_readings[i] + readings[i] for i in range(self.num_sensors)]
            # average sampled readings
        self.white_values = [val // samples for val in avg_readings]
        # update value of self.white_values
        print(f'white calibration complete: {self.white_values}\n')
        # let user know calibration is complete and display calibrated values
    
    def calibrate_black(self, samples=100):
        '''calibrates the sensor array for a black surface
            inputs:
                - samples
                    value of desired samples
                    predefined as 100
            functionality:
                - allows user to set up and calibrate on black surface
                - averages the sensor reading values for a black surface  
                - updates self.black_values based on what sensors actually see
            outputs:
                - N/A
        '''
        print('place the sensor over a BLACK surface and press ENTER')
        # prompt user
        input()
        # wait for user confirmation
        print('calibrating black values...')
        # tell user calibration has started
        avg_readings = [0] * self.num_sensors
        # create list for number of sensors
        for _ in range(samples):
        # iterate for the number of specified samples
            readings = [sensor.read() for sensor in self.sensors]
            # read sensor data while on a black surface
            avg_readings = [avg_readings[i] + readings[i] for i in range(self.num_sensors)]
            # average sampled readings
        self.black_values = [val // samples for val in avg_readings]
        # update value of self.black_values
        print(f'black calibration complete: {self.black_values}\n')
        # let user know calibration is complete and display calibrated values

    def get_centroid(self):
        '''get_centroid function computes the centroid of the detected line
            inputs:
                - N/A
            functionality:
                - computes weighted sum of sensor positions and their readings
                - computes total sensor readings
                - accounts for detection of no line
                - returns centroid value
            outputs:
                - centroid: value of where the centroid falls between the sensor array
        '''
        readings = self.read_sensors()
        # gets sensor readings

        # define weights for 8-channel sensor
        weights = [-12, -9, -6, -3, 3, 6, 9, 12]

        # check if the number of weights matches the number of sensors
        if len(weights) != self.num_sensors:
            raise ValueError('number of weights must match number of sensors')

        # calculate weighted sum and total intensity
        weighted_sum = sum(weights[i] * readings[i] for i in range(self.num_sensors))
        total = sum(readings)
        
        # handle case where no line is detected
        if total == 0:
            print('WARNING: No line detected!')
            return 0  # return 0 to indicate the line is not detected

        # calculate and return the centroid position
        centroid = weighted_sum / total
        return centroid