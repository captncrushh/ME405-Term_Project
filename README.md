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
Task Diagram<br/>
![ME405 - Term Project Task Diagram](https://github.com/user-attachments/assets/a7b19dc2-1fdd-473a-a4ac-508d5f496fe6)<br/>

Controls Task<br/>
![ME405 - Term Project Controls Task](https://github.com/user-attachments/assets/c69e06ab-3ef6-47f8-84b8-9d2517bd0bf8)<br/>

Motor Task<br/>
![ME405 - Term Project Motor Task](https://github.com/user-attachments/assets/86c5ae5c-04f3-4b7c-b392-78456e249069)<br/>

## :clipboard: Requirements & Considerations :clipboard: <br/> 
// yap here
### :stopwatch: Time-Trial Track :stopwatch: <br/>
![image](https://github.com/user-attachments/assets/e8a353c0-c669-417b-954b-f5ed3fb6d694) <br/>
## :movie_camera: Demonstrations :film_strip: <br/>
+ add in the video of it doing the track in reverse for fun <br/>
+ add in the video of it complementing the track <br/>
[![Track Trial](https://img.youtube.com/shorts/YOb_HbBaUi0?si=EPy07hzMK3LaYQmP/0.jpg)](https://www.youtube.com/watch?v=YOb_HbBaUi0?si=EPy07hzMK3LaYQmP)
|Trial| CP#1| CP#2| CP#3| CP#4| CP#5| CP#6|Cups |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|  1  |12.40|23.97|35.98|41.01|47.37| N/A |0    |    
|  2  |14.17|26.89|37.76|45.45|49.25| N/A |0    |     
|  3  |14.62|26.89|38.06|46.09|50.05| N/A |0    |   
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
