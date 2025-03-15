
# Lab 0x02 - Writing Hardware Drivers   
# MECHA 36: Emily Nicoletta & Beneda Loya
# encoder class

from pyb import Pin, Timer
from time import ticks_us, ticks_diff, ticks_add 
# Use to get dt value in update()
# import classes and modules

class Encoder:
    '''A quadrature encoder decoding interface encapsulated in a Python 
       class'''

    def __init__(self, tim, chA_pin, chB_pin):
        '''Initializes an Encoder object'''
        
        # encoder pins
        self.ENA_pin = Pin(chA_pin, mode=Pin.IN)
        self.ENB_pin = Pin(chB_pin, mode=Pin.IN)

        # encoder timer setup
        self.ENC_TIM = Timer(tim, period=0xFFFF, prescaler=0)
        self.ENC_TIM.channel(1, pin=self.ENA_pin, mode=Timer.ENC_AB)
        self.ENC_TIM.channel(2, pin=self.ENB_pin, mode=Timer.ENC_AB)

        self.position = 0 # Total accumulated position of the encoder
        self.prev_count = 0 # Counter value from the most recent update
        self.delta = 0 # Change in count between last two updates
        self.dt = 0 # Amount of time between last two updates

    def update(self):
        '''Runs one update step on the encoder's timer counter to keep
           track of the change in count and check for counter reload'''

        AR = 0xFFFF # set auto-reload value to highest 16 bit number

        curr_time = ticks_us()
        curr_count = self.ENC_TIM.counter() # current timer counter value
        
        self.delta = curr_count - self.prev_count

        if self.delta > (AR + 1) / 2:
            self.delta = self.delta - (AR + 1)

        elif self.delta < -((AR + 1) / 2):
            self.delta = self.delta + (AR + 1)

        self.prev_time = 0
        self.dt = ticks_diff(curr_time, self.prev_count) / 1_000_000
        self.prev_time = curr_time
        self.prev_count = curr_count # current count become previous count
        self.position += self.delta  # Update position
        
    def get_position(self):
        '''Returns the most recently updated value of position as determined
           within the update() method'''

        return self.position
    
    def get_velocity(self):
        '''Returns a measure of velocity using the the most recently updated
           value of delta as determined within the update() method'''

        if self.dt > 0:
        # to handle division by 0 errors
            return self.delta/self.dt
        else:
            return 0 

    
    def zero(self):
        '''Sets the present encoder position to zero and causes future updates
           to measure with respect to the new zero position'''
        self.position = 0
        self.prev_count = self.ENC_TIM.counter()  # Ensure updates remain consistent
