# term project
# bump sensor driver class
# Emily Nicoletta, Bea Loya
# 02/27/2025

# import libraries/classes
from pyb import Pin

'''
# define bump sensor channel pins
L_BMP5 = 'C8'
L_BMP4 = 'B2'
L_BMP3 = 'B15'
R_BMP2 = 'H0'
R_BMP1 = 'B7'
R_BMP0 = 'A15'

# put sensor pins in a list to be passed to LineSensor class
bump_sensor_pins = [L_BMP5, L_BMP4, L_BMP3, R_BMP2, R_BMP1, R_BMP0]
'''

class BumpSensor:
    ''' bump sensor driver class 
        functionalites:
            - reads sensor values and returns them as a 6 bit binary output
                active low switches so will output 0 is pressed or bumped
                meaning since they are normally high they require PULL_UPs
            - prints sensor status to the terminal and a binary output
            - enables interrupts for better handling of switch changes
    '''
    def __init__(self, sensor_pins):
        ''' bump sensor object instantiation
            inputs:
                - sensor_pins:
                    list of pin names where sensors channels are connected
            functionality:
                - define pins as input with PULL_UPs since active low switches
                - define status as 0 to act as a bitmask for bump sensor states
            outputs:
                - N/A
        '''
        # self attributes
        self.sensors = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in sensor_pins]
        # define each pin in the sensor pin list as an input with PULL_UPs Pin
        self.status = 1
        # define status as 1 - bitmask for bump sensor states

    def read_sensors(self):
        '''read_sensors method gets current sensor data
            inputs:
                - N/A
            functionality:
                - read all bump sensors 
                - bitmask sensor values
            outputs:
                - return self.status:
                    bitmask representing active sensors
        '''
        self.status = 0
        # ensure self.status is declared as 0
        for i, pin in enumerate(self.sensors):
        # for each index and pin in the sensor list
            if pin.value() == 0:
            # check if 0 or active-low (pressed)
                self.status |= (1 << i)
                # |= is bitwise or
                # (1 << i) shifts 1 left by i places, creating a bitmask
        return self.status
    
    def print_status(self):
        '''print_status method prints the status of the bump sensors
            inputs:
                - N/A
            functionality:
                - print the current bump sensor status in binary
            outputs:
                - N/A
        '''
        print(f"Bump Sensor Status: {bin(self.read_sensors())}")


def main():
    # define bump sensor channel pins
    L_BMP5 = 'C8'
    L_BMP4 = 'B2'
    L_BMP3 = 'B15'
    R_BMP2 = 'H0'
    R_BMP1 = 'B7'
    R_BMP0 = 'A15'

    # put sensor pins in a list to be passed to LineSensor class
    bump_sensor_pins = [R_BMP0, R_BMP1, R_BMP2, L_BMP3, L_BMP4, L_BMP5]
    # right to left

    bump_sensor = BumpSensor(bump_sensor_pins)
    # initialize bump sensor object

    while True:
    # continuous while loop
        bump_sensor.print_status()

if __name__ == "__main__":
    main()

    