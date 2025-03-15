# lab0x04 
# PID class
# Emily Nicoletta, Bea Loya
# 02/20/2025

class PIDcontroller:
    ''' PID controller class 
        functionalites:
            - calculate PID controller output for a given error
    '''
    def __init__(self, Kp, Ki, Kd):
        ''' PID controller object instantiation
            inputs:
                - Kp:
                    proportional gain
                - Ki:
                    inetegral gain
                - Kd:
                    derivative gain
            functionality:
                - initializing variables
            outputs:
                - N/A
        '''
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.prev_error = 0
        self.integral = 0
    
    def compute_pid(self, error, dt):
        ''' compute_pid methods calculates the PID control output using error
            inputs:
                - error:
                    error value from desired value
                - dt:
                    time since last update
            functionality:
                - calculates proportional control
                - calculates integral control
                    accumulate errors over time
                -calculates derivative control
                    difference between current and previous error over time
                - sums P I D terms
            outputs:
                - PID:
                    controller output to be applied to input to fix error
        '''
        # proportional term
        P = self.Kp * error
        
        # integral term
        self.integral += error * dt
        # accumulate errors over time
        I = self.Ki * self.integral
        
        # derivative term
        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        # difference between current and previous error over time
        D = self.Kd * derivative

        PID = P + I + D
        # sum of PID terms

        self.prev_error = error
        # set previous error to current error
        return PID
        # return PID controller output
