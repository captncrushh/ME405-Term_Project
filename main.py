# lab0x04 
# main python file
# Emily Nicoletta, Bea Loya
# 03/11/2025

# import libraries/classes
from pyb import Pin, I2C, delay
from time import ticks_us, ticks_diff

from motor import Motor
from encoder import Encoder
from line_sensor import LineSensor
from PID import PIDcontroller
from BNO055_Driver_Class import BNO055
# import drivers

# from line_sensor_task import LineSensorTask as LST
# from PID_task import PIDControllerTask as PIDCT
# from motor_task import MotorTask as MT
# import tasks

import cotask as ct
import task_share as ts
# import cotask and task_share for multitasking via priority scheduling


## define pin connections
# left motor and encoder configuration
ELA = "A1"
ELB = "A0"
L_SLP = "B6"
L_DIR = "B5"
L_PWM = "B4"
L_ENC_Timer = 2
L_PWM_Timer = 3

# right motor and encoder configuration
ERA = "C7"
ERB = "C6"
R_SLP = "H1" # changed from lab0x03
R_DIR = "C3"
R_PWM = "A6"
R_ENC_Timer = 8
R_PWM_Timer = 3

# define pwm channel
pwm_channel = 1

# define sensor channel pins
C0 = Pin.cpu.C0
B0 = Pin.cpu.B0
A4 = Pin.cpu.A4
C5 = Pin.cpu.C5
A7 = Pin.cpu.A7
B1 = Pin.cpu.B1
C4 = Pin.cpu.C4
C2 = Pin.cpu.C2
CTRL = Pin.cpu.C9

# for ease of object instantiation
R_M_PINS = (R_PWM, R_DIR, R_SLP, R_PWM_Timer, pwm_channel)
L_M_PINS = (L_PWM, L_DIR, L_SLP, L_PWM_Timer, pwm_channel)

R_ENC_PINS = (R_ENC_Timer, ERA, ERB)
L_ENC_PINS = (L_ENC_Timer, ELA, ELB)

line_sensor_pins = [C0, B0, A4, C5, A7, B1, C4, C2]

# instantiate motors
left_motor = Motor(*L_M_PINS)
right_motor = Motor(*R_M_PINS)

# instantiate encoder objects
right_encoder = Encoder(*R_ENC_PINS)
left_encoder = Encoder(*L_ENC_PINS)

# instantiate line sensor
line_sensor = LineSensor(line_sensor_pins)

# instantiate PID controller with tuned values
PID_controller = PIDcontroller(Kp=5.5, Ki=5, Kd=0)
# goodish one
# Jack recommends adding in Kd = 2 and see what happeneds
# We prob should increase Kp'
#PID_controller = PIDcontroller(Kp=1.5, Ki=0, Kd=1.1)

# Initialize I2C and IMU
i2c = I2C(1, I2C.CONTROLLER)
imu = BNO055(i2c)
last_val = 0xFFFF
devices = i2c.scan()

## shared variables and queues
error = ts.Share('f', thread_protect=True, name='error')
# error value
correction = ts.Share('f', thread_protect=True, name='controller output')
# controller output value

def Controls():
    while True:
        ctrd = line_sensor.get_centroid()
        # calculate centroid from sensor data
        # print(line_sensor.read_sensors())
        # print sensor readings for debugging
        print(f'centroid: {ctrd}')
        # print centroid value for debugging
        t1 = ticks_us()
        # get the start time
        err = ctrd
        # centroid directly represents the error
        print(f'error: {err}')
        # print error value for debugging
        t2 = ticks_us()
        # get the current time
        dt = ticks_diff(t2, t1) / 1_000_000  
        # calculate the difference in time between calculation readings
        # converted to seconds
        controller_output = max(-50, min(50, PID_controller.compute_pid(err, dt)))
        # calculate the controller output based on error and time
        # add clamps to prevent too high of output
        t1 = t2
        # shift times so current time become previous time
        error.put(err)
        correction.put(controller_output)
        # put data in shares
        yield 

def pivot_to_zero():
    left_motor.enable()
    right_motor.enable()
    # print("Motors enabled, starting pivot...")

    previous_error = 0
    Kp = 1.5  # Proportional gain
    Kd = 1.1  # Derivative gain

    while abs(( (zero) - imu.get_heading()) % 360)> 5:  # Small tolerance to stop
        error =  ( (zero) - imu.get_heading()) % 360
        derivative = error - previous_error
        
        # PD control: effort is scaled by error and derivative term
        effort = max(10, min(30, abs(Kp * error + Kd * derivative)))
        if error < 0:
            effort = -effort  # Adjust for direction
        
        print(f"Setting motor efforts: {effort}, {-effort}")  # Debugging
        left_motor.set_effort(effort)
        right_motor.set_effort(-effort)
        delay(50)  # Small delay to stabilize readings
        
        previous_error = error  # Update previous error

    left_motor.set_effort(0)
    right_motor.set_effort(0)
    # print("Pivot complete, motors stopped.")

S0_LINE = 0
S1_ZERO = 1
S2_GRID = 2



# MotorTask to apply the PID controller output to the motor voltages
def MotorTask():
    global state
    while True:
        base_effort = 15
        # set a base effort of 20%
        err = error.get()
        # get the error value from the share
        controller_output = correction.get()
        # get the controller output value from the share
        print(f'error: {err} \ncontroller output: {controller_output}')  
        # print statement for debugging

        if (state == S0_LINE):
            if (left_encoder.position > 25498 or right_encoder.position > 22229):
                state = S1_ZERO
            if (err < -3.5 or err > 3.5): 
                # apply controller outputs to effort 
                left_effort = base_effort + controller_output
                # adjust left effort by controller output
                right_effort = base_effort - controller_output
                # adjust right effort by controller output
                
                # cap efforts to prevent overdriving the motors
                left_effort = max(-60, min(60, left_effort))
                right_effort = max(-60, min(60, right_effort))
                
                print(f'left effort: {left_effort}, right effort: {right_effort}')  
                # print statement for debugging
                
                left_motor.enable()
                # enable left motor
                right_motor.enable()
                # enable right motor
                left_motor.set_effort(left_effort)
                # set left motor effort to calculated left effort
                right_motor.set_effort(right_effort)
                # set right motor effort to calculated right effort
                left_encoder.update()
                right_encoder.update()
                print(f'l enc: {left_encoder.position}, r enc: {right_encoder.position}')
                # print encoder positions
            else:
                # error is 0, so romi is centered on line
                # drive straight since already centered/to stay centered
                left_motor.enable()
                # enable left motor
                right_motor.enable()
                # enable right motor
                left_motor.set_effort(base_effort)
                # set left motor effort to base effort
                right_motor.set_effort(base_effort)
                # set right motor effort to base effort
                left_encoder.update()
                right_encoder.update()
                print(f'l enc: {left_encoder.position}, r enc: {right_encoder.position}')
                # print encoder positions


        elif (state == S1_ZERO):
            imu.set_mode(BNO055.MODE_CONFIG)  # Reset IMU
            delay(500)
            imu.set_mode(BNO055.MODE_NDOF)    # Restart in sensor fusion mode
            delay(500)
            
            pivot_to_zero()

            left_encoder.zero()
            right_encoder.zero()

            state = S2_GRID


        elif (state == S2_GRID):
       
            left_motor.set_effort(base_effort)
            # set left motor effort to base effort
            right_motor.set_effort(base_effort)
            # set right motor effort to base effort

            left_encoder.update()
            right_encoder.update()
            print(f'l enc: {left_encoder.position}, r enc: {right_encoder.position}') 

        yield

# main function code
def main():
    global state
    state = 0

    ## create tasks
    controls_task = ct.Task(Controls, 
                    name='line sensor task', 
                    priority=1, 
                    period=15,
                    profile=True,
                    trace=True)
    motor_task = ct.Task(MotorTask, 
                    name='motor task', 
                    priority=1, 
                    period=20,
                    profile=True,
                    trace=True)
    
    # add tasks to scheduler
    ct.task_list.append(controls_task)
    ct.task_list.append(motor_task)

    # prompt user to calibrate white and black surfaces
    line_sensor.calibrate_white()
    # calibrate white surface
    line_sensor.calibrate_black()
    # calibrate black surface
    
    imu.set_mode(BNO055.MODE_CONFIG)  # Reset IMU
    pyb.delay(500)
    imu.set_mode(BNO055.MODE_NDOF)    # Restart in sensor fusion mode
    pyb.delay(500)
    
    sys, gyro, accel, mag = imu.get_calibration_status()
    print(f"Calibration Status - SYS: {sys}, GYRO: {gyro}, ACCEL: {accel}, MAG: {mag}")
    print("\n")

    print(f"Detected I2C devices: {devices}")
    
    # pront user to get heading 
    print("\nplace romi for zero heading")
    # prompt
    input()
    # wait for user confirmation via keyboard inputs

    global zero
    zero = imu.get_heading()
    # get current heading angle
    print(zero)
    # print zero heading


    # prompt user to place romi in line to follow
    print("\nplace romi on line to follow and press ENTER")
    # prompt
    input()
    # wait for user confirmation via keyboard inputs
    print("following line...\n")
    # indicate start of scheduler and that romi should be following line

    # start scheduler
    while True:
        try:
            ct.task_list.pri_sched()
        except KeyboardInterrupt:
            left_motor.disable()
            right_motor.disable()
            print('\n' + str(ct.task_list))
            print(ts.show_all())
            # print task info
            break
        except:
            left_motor.disable()
            right_motor.disable()
            print('\n' + str(ct.task_list))
            print(ts.show_all())
            # print task info
            raise
        
if __name__ == "__main__":
    main()