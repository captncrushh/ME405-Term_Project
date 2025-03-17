# ME405: Term Project
### Romi Time-trials & Demonstrations
By: Emily Nicoletta & Beneda Loya <br/>Instructor: Charlie Refvem<br/> 
***
## :monocle_face: Overview :monocle_face:
Our term project focuses on building and demonstrating a time-trial showcasing the mechanical and electrical design we implemented. This project is to present all of the useful tools and skills we have learned from all of the labs we have done this quarter.
## :classical_building: System Architecture :classical_building:
###  :robot: Our Wild Child of a Romi :robot:
<img src="https://github.com/user-attachments/assets/220ccc75-52e3-466b-ba17-f61fb5f1a81c" width="600" height ="550" /> <br/>
### :gear: Hardware :gear:
+ Romi Chassis kit -> [x](https://www.pololu.com/product/3504) <br/>
+ Motor Driver and Power Distribution Board -> [x](https://www.pololu.com/product/3543) <br/>
+ QTRX-MD-08A Reflectance Sensor Array: 8 Channel -> [x](https://www.pololu.com/product/4448) <br/>
+ Left Bumper switch Assembly -> [x](https://www.pololu.com/product/3673) <br/>
+ Right Bumper switch Assembly -> [x](https://www.pololu.com/product/3674) <br/>
+ Crimp Connector Housing ( 1x6, 2x6, 2x13 ) -> [x](https://www.pololu.com/product/1905) <br/>
+ Dupont Ribbon -> [x](https://www.amazon.com/dp/B07GCY6CH7) <br/>
+ NiMH AA Batteries -> [x](https://www.amazon.com/dp/B0D2JCY87L) <br/>
+ NiMH Battery Charger -> [x](https://www.amazon.com/dp/B00JHKSLM8) <br/>
+ Heat Shrink Tubing -> [x](https://www.amazon.com/dp/B01MFA3OFA) <br/>

### :knot: Wiring Diagram :knot:
![circuit](https://github.com/user-attachments/assets/f66a9238-a684-49f4-97ae-08b2e2db9ae0) <br/>
To see a more detailed version of the Nucleo Pinouts click here -> [X](https://os.mbed.com/platforms/ST-Nucleo-L476RG/#microcontroller-features) <br/>
Here is the pin connections in table format below!
![image](https://github.com/user-attachments/assets/554a8914-a075-42b0-800b-c046ddf610f1)
### :computer: Code :snake:
Our Romi uses motor, encoder, line sensor, bump sensor, and an BNO055 imu driver for line tracking based motion as well as imu heading and encoder postion tracking motion. We developed these drivers and use given cotask and task_share files to perform priority scheduling based multitasking. In the end, we did not have funcionality to have the bump sensors to interrupt motion. However, the line tracking motion used a tuned proportional-integral-derivative (PID) controller to allow for smoother motion. Additonally, we were able to use the imu to get heading readings to direct the Romi in a specific direction and use the encoders on each wheel to track the the distance the Romi moves given a certain amount of ticks. 
<br/>
<br/>
To see all of our code in one place click here -> [x](https://github.com/captncrushh/ME405-Term_Project/tree/main/Term_project_Code)
+ `main.py` -> [x](https://github.com/captncrushh/ME405-Term_Project/blob/main/Term_project_Code/main.py)
   - Main program that handles the functionality of Romi's behavior
+ `motor.py` -> [x](https://github.com/captncrushh/ME405-Term_Project/blob/main/Term_project_Code/motor.py)
   - Controls our motor operations
+ `encoder.py` -> [x](https://github.com/captncrushh/ME405-Term_Project/blob/main/Term_project_Code/encoder.py)
   - A quadrature encoder decoding interface encapsulated in a Python class
+ `line_sensor.py` -> [x](https://github.com/captncrushh/ME405-Term_Project/blob/main/Term_project_Code/line_sensor.py)
   - Line sensor driver class that reads sensor values and normalizes raw sensor values from 0 to 1, calibrates for white & black surfaces, and calculates our centroid
+ `bump_sensor.py` -> [x](https://github.com/captncrushh/ME405-Term_Project/blob/main/Term_project_Code/bump_sensor.py)
   - Bump sensor driver class that reads sensor values and returns them as a 6-bit binary output
+ `PID.py` -> [x](https://github.com/captncrushh/ME405-Term_Project/blob/main/Term_project_Code/PID.py)
   - PID controller class that calculates PID controller output for a given error
+ `BNO055_Driver_Class.py` -> [x](https://github.com/captncrushh/ME405-Term_Project/blob/main/Term_project_Code/BNO055_Driver_Class.py)
   - Interfaces the BNO055 sensor
+ `cotask.py` -> [x](https://github.com/captncrushh/ME405-Term_Project/blob/main/Term_project_Code/cotask.py)
   - Manages cooperative multitasking: written by JR Ridgely 
+ `task_share.py` -> [x](https://github.com/captncrushh/ME405-Term_Project/blob/main/Term_project_Code/task_share.py)
   - Facilitates shared data between tasks: written by JR Ridgely
### :memo:Code Functionality :memo:
+ ***Main*** <br/>
Before running the tasks, the main code prompts the user to help calibrate the Romi before starting. This includes white and black surface calibration for the line sensor as well as imu calibration and calibration of reference heading angles. <br/> <br/>
+ ***Task Diagram*** <br/>
Our main.py files houses both the controls task and motor task. We were unsuccesful implementing tasks as individual classes in seperate python files and ultilizing instances of them. So, we choose to implement task simply as functions in the main python file. We still used shares for variables used across both functions (error, controller output), but some other variables that are attributes of other object instances are just called when they should maybe be a share or queue (motor efforts, encoder positions). Additionally, we struggled a little bit with the timing and priorties of the tasks. We used the trace printed in the terminal at the end of each run to determine the average and maximum run times for each task and ajusted the periods accordingly. Knowing the timing allowed us to ensure that wer were giving enough time for the task to fully run before alternating to the other task. Furthermore, we ended up having both tasks being the same priority meaning that theyr would juse run round-robin style with each other. We found that changing the priority would result in lower priority task not running at all. <br/> <br/>
  ![ME405 - Term Project Task Diagram](https://github.com/user-attachments/assets/a7b19dc2-1fdd-473a-a4ac-508d5f496fe6)<br/>

+ ***Controls Task*** <br/>
The controls task records the current time and gets the centroid value from the line sensor, then sets the error equal to the centroid value and records the time again. Next, it computes the controller output values using the error and difference in recorded times. The error value and controller ourput value are them put into shares so that they can be used by the motor task. In this task, the controller output is capped between -50 and 50. We did a lot of trial and error tuning with the PID gains, and a lot of the time when including all Kp, Ki, and Kd constants, the controller output was very large. So, when applying it the the motors there was great differences between the motor outputs. This resulted in a lot of overcorrection and jerky movements. <br/> <br/>
  ![ME405 - Term Project Controls Task](https://github.com/user-attachments/assets/c69e06ab-3ef6-47f8-84b8-9d2517bd0bf8)<br/>

+ ***Motor Task*** <br/>
The motor task is implemented as a finite state machine (FSM) to account for all the 'stages' Romi goes throught to complete the course. The first state, S0_LINE, is to be used for the entirety of the line tracking portion of the game track or up until checkpoint 4. First it checks if the encoders have reached the value they are supposed to be at once it reaches checkpoint 4 which was found after a lot of trial and error and validation checking. If not it continues by checking what the error value is. If it is outisde the bounds of -3.5 to 3.5 the controller output value is applied to a base motor effort appropriately so that Romi will become more centered. Limits of -60 to 60 were put on to the adjusted motor effort values as well to account for large controller output values. This help prevent the Romi from extreme and jerky movements. However, if the error was within the bounds, meaing it was close to being centered already, the Romi was commanded to just drive straight. Once it readched the number of encoder ticks it normally takes to get to checkpoint 4, it moves to the next state, S1_STRAIGHTEN, where it adjusts the heading angle (using a pre-calibrated heading value) to ensure Romi drives straight through the grid caged section of the game track. Then it enters the next state, S2_GRID, where the Romi drive forward and keeps track of the neumber of encoder ticks to get to the end of the grid section and to turn to checkpount 5. In the next state, S3_turn, it uses another pre-calibrated heading angle to face checkpoint 5. In state S4_TO_WALL, again it uses monitoring of encoder ticks to control how far Romi should go to drive it through checkpoint 5 and to the wall. Ideally this state would use the bump sensors to determine when it got to the wall and control its corresponding movements, but we ran out of time to implement this. So then in the next state S5_BACK, the Romi is commanded to reverse backwards for 500 encoder ticks to give some creance form the wall. Next, in state S6_STOP, the motor efforts are set to 0 to stop movement. In the end, we weren't fully able to implement all the states we wanted to complete the game track. We found that using the imu heading angle and encoder ticks for distance wasn't as straight forward as we thought and ultimately ran out of time. We had trouble making sure the the Romi actually oriented correctly during the first turn at checkpoint 4 before the grid and then going straight afterwards. We believe we might have gotten a robot with a wonky wheel (it was suggested before that the left weel was wobbly and that Romi could have been dropped in a previous quarter) or that the motor gains were gretly different from each other meaning that given the same effort, Romi would not drive straight. We tried to account for the motor gains by adjusting the motor effort in the individual state itself. <br/>
We drafted some code for the rest of the states that the Romi would theoretically need to go around the wall and end in the finish location. It uses the same logic of a state used for turning to a pre-calibrated heading angle and the another state for driving for a certain amount of encoder ticks. This is shown both here in the task diagram in dashed lines as well as in the code in a commented out code block. We tested it once with the full implementation of code, but did not actually measure the encoder ticks necessary for the distances to go around the wall. Additionally, since we were having issues ensuring it always oriented to the desred angle and actually driving in a straight line, it did not perform to its highest capabilites. Given more time to tune and test, we believe we could have had the Romi working for the full game course. <br/> <br/>
  ![ME405 - Term Project Motor Task](https://github.com/user-attachments/assets/86c5ae5c-04f3-4b7c-b392-78456e249069)<br/>

## :clipboard: Requirements & Considerations :clipboard: <br/> 
// yap here
### :stopwatch: Time-Trial Track :stopwatch: <br/>
![image](https://github.com/user-attachments/assets/e8a353c0-c669-417b-954b-f5ed3fb6d694) <br/>
## :movie_camera: Demonstrations :film_strip: <br/>
### Timed Track Trial
[![Track Trial](https://img.youtube.com/vi/YOb_HbBaUi0/0.jpg)](https://www.youtube.com/watch?v=YOb_HbBaUi0) <br/>
### Timed Theoretical Trial
[![Theoretical Trail](https://img.youtube.com/vi/foPPc98IBt8/0.jpg)](https://www.youtube.com/watch?v=foPPc98IBt8) <br/>

|Trial               |                CP#1| CP#2| CP#3| CP#4| CP#5| CP#6|Cups |
|:---:               |               :---:|:---:|:---:|:---:|:---:|:---:|:---:|
|  1                 |               12.40|23.97|35.98|41.01|47.37| N/A |0    |    
|  2                 |               14.17|26.89|37.76|45.45|49.25| N/A |0    |     
|  3                 |               14.62|26.89|38.06|46.09|50.05| N/A |0    |
|  Theoretical trial |               10.96|21.40|33.67|41.70|46.58|57.01|"1"  |

***:star2:Bonus Video!!!:star2:*** **Can others say their Romi can do the track in REVERSE? We didn't think so :relieved:** <br/>
In this video, Romi is able to do the track starting from checkpoint 5 to the beginning using only the IR Sensor!!! <br/>
*Of course with the exception of needing some nudges here and there.* <br/>
(The code implemented in this video is an old version of what we currently have.)
[![Track Trial](https://img.youtube.com/vi/kFxPreD4h78/0.jpg)](https://www.youtube.com/watch?v=kFxPreD4h78) <br/>

## :sparkles: Romi's Photoshoot :sparkles: <br/>
### *Enhanced Version*
<img src="https://github.com/user-attachments/assets/e05df955-db58-41e5-afab-6081f345df11"/> <br/>
<img src="https://github.com/user-attachments/assets/e05df955-db58-41e5-afab-6081f345df11"/> <br/>
<img src="https://github.com/user-attachments/assets/e05df955-db58-41e5-afab-6081f345df11"/> <br/>
<img src="https://github.com/user-attachments/assets/b37fc313-4af6-4dae-9e3e-6113da41b985"/> <br/>
<img src="https://github.com/user-attachments/assets/dd33e3e7-bc5a-49cd-a98b-9151e1460042"/> <br/>
<img src="https://github.com/user-attachments/assets/11d5cb79-133a-4164-8126-b4ad1f7bad37"/> <br/>
<img src="https://github.com/user-attachments/assets/070a01d1-c2ce-4e09-8eff-c57bbd93a4c1"/> <br/>
<img src="https://github.com/user-attachments/assets/ecc40139-0366-4708-9ea3-1445a0d84e5d"/> <br/>
