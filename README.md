# RubikSolver

Simple Python & C++ (Arduino) Rubik's Cube Solver
It's just like many other Rubik's cube solvers that you have already seen on the internet.
Everything was coded by myself, no copy-and-paste or anything like that.
I sure referenced documentation, forums and tutorials to make it work.
I tried to coded as simple as possible without losing performance (even tho it's not the best performing code possible, obviously)

I used the following libraries:
- Kociemba
- PySerial
- Time

# brain.py
This file contains just the "frontend" part of the project. It uses classes from the models.py file to solve the cube.

# models.py
This file contains all the models I created to simplify and clear the code as much as possible.

- Port: connect to the USB port, sends and receives data to and from the arduino and resets the arduino.
- Koci: solves the rubik's cube and converts the string given by the Kociemba module into an array
- Motor: sends data to the arduino depending on the array given by the Koci class. It uses the Port class to do so.
- Solver: connects to the Arduino, then solves the cube using all the previous models.

# arduino.ino
This file contains all the code for the Arduino.
It first flashes the built-in LED a couple of times, then it sends a "start" command to Python (which is listening to it). This confirms that the Arduino is connected and responding.
Then the code listens to any incoming data from the USB.
The data will always begin with a "!" and end with a ";".

Currently the motors are not activated. The code just sends back to Python the same commands it received (this was needed for debugging and will be removed)
