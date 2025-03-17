# ME405: Term Project
### Romi Time-trials & Demonstrations
By: Emily Nicoletta & Beneda Loya <br/>Instructor: Charlie Refvem<br/> 
***
## :monocle_face: Overview :monocle_face:
Our term project focuses on building and demonstrating a time-trial showcasing the mechanical and electrical design we implemented. This project is to present all of the useful tools and skills we have learned from all of the labs we have done this quarter.
## :classical_building: System Architecture :classical_building:
###  :robot: Our Wild Child of a Romi :robot:
// insert pictures of Romi here!!

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
// add in a summary of the overall function of our code here! <br/>
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
// add in diagrams like FSM, Schuedler ..etc
// maybe also add in a brief summary of what each py file does??
## :clipboard: Requirements & Considerations :clipboard: <br/> 
// yap here
### :stopwatch: Time-Trial Track :stopwatch: <br/>
![image](https://github.com/user-attachments/assets/e8a353c0-c669-417b-954b-f5ed3fb6d694) <br/>
## :movie_camera: Demonstrations :film_strip: <br/>
// add in the video of it doing the track in reverse for fun
// add in the video of it complementing the track
// add in the times for romi
## :sparkles: Romi's Photoshoot :sparkles: <br/>
![IMG_6389](https://github.com/user-attachments/assets/b37fc313-4af6-4dae-9e3e-6113da41b985)
![IMG_6391](https://github.com/user-attachments/assets/dd33e3e7-bc5a-49cd-a98b-9151e1460042)
![IMG_6393](https://github.com/user-attachments/assets/11d5cb79-133a-4164-8126-b4ad1f7bad37)
![IMG_6395](https://github.com/user-attachments/assets/070a01d1-c2ce-4e09-8eff-c57bbd93a4c1)
![IMG_6396](https://github.com/user-attachments/assets/ecc40139-0366-4708-9ea3-1445a0d84e5d)
