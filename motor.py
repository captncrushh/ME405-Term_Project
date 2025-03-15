
# Lab 0x02 - Writing Hardware Drivers   
# MECHA 36: Emily Nicoletta & Beneda Loya
# motor class

from pyb import Pin,Timer
# import class modules

class Motor:
    '''A motor driver interface encapsulated in a Python class. Works with
       5 motor drivers using separate PWM and direction inputs such as the 
       DRV8838 6 drivers present on the Romi chassis from Pololu.'''

    def __init__(self, PWM, DIR, nSLP, PWM_TIM, PWM_CH):
        '''Initializes a Motor object'''
        
        # motor control pins
        self.nSLP_pin = Pin(nSLP, mode=Pin.OUT_PP, value=0)
        self.PWM_pin = Pin(PWM, mode=Pin.OUT_PP, value=0)
        self.DIR_pin = Pin(DIR, mode=Pin.OUT_PP, value=0)
        
        # PWM timer setup
        self.pwm_timer = Timer(PWM_TIM, freq=22000)  # set frequency to 1 kHz
        self.pwm_channel = self.pwm_timer.channel(PWM_CH, 
                                                  Timer.PWM, 
                                                  pin=self.PWM_pin)

    def set_effort(self, effort):
        '''Sets the present effort requested from the motor based on an input 
           value between -100 and 100'''
        
        if effort >= 0 and effort <= 100: # effort is positive value
            self.DIR_pin.low() # wheels spin forward
            self.pwm_channel.pulse_width_percent(effort) 
            # wheels spin at specified effort speed

        elif effort < 0 and effort >= -100: # effort is negative value
            self.DIR_pin.high() # wheels spin backward
            self.pwm_channel.pulse_width_percent(abs(effort))
            # wheels spin at specified effort speed

        # else: # else if effort is 0 or absolute value greater than 100 percent
        #     self.disable() # stop motors
        # changed for term project - don't disable when 0

    def enable(self):
        '''Enables the motor driver by taking it out of sleep mode into brake 
           mode'''
        
        self.nSLP_pin.high()


    def disable(self):
        '''Disables the motor driver by taking it into sleep mode'''
        
        self.pwm_channel.pulse_width_percent(0)
        self.nSLP_pin.low()