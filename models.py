#!/usr/bin/env python3

# Dependencies
from serial import Serial # Connects to the USB and communicates with the Arduino
from kociemba import solve # Given a scrumble returns a string containing the solution in the official notation
from time import sleep # Stops the Python script for N seconds eg. sleep(N)

class Port():
    
    """
        Directly handles the serial communication with Arduino by sending and receiving data.
        Can reset Arduino.
    """
    
    def __init__(self, port: str, rate=9600, timeout=1): # eg. port = '/dev/ttyACM0'
        self.port = Serial(port, rate, timeout=timeout) # Try to connect with the Arduino
        sleep(2) # Wait some time to let the connection happen
        
        self.is_responsive = False
    
    def send(self, data: str): # Send a string to Arduino in binary (ASCII encoding)
        self.port.write(bytes(data, 'ascii'))
        
    def get(self):
        if self.port.inWaiting() > 0: # Check if there is any incoming serial data
            return self.port.read(self.port.inWaiting()) # Return the received data
        return ''

    def waiting(self):
        return self.port.inWaiting()
    
    def reset(self): # Reset the Arduino
        self.port.setDTR(False)
        sleep(1)
        self.port.flushInput()
        self.port.setDTR(True)
        
    def connect(self, reset: bool) -> None:
        if reset:
            self.reset()
        
        while not self.is_responsive:
            while self.waiting():
                if self.get().decode('ascii') == '!':
                    self.is_responsive = True
                    print('Arduino is connected and responsive.')
                else:
                    print('Arduino is connected, but unresponsive.')
    
class Motor():
    
    def __init__(self, pin: int, port: Port):
        self.pin = pin
        self.port = port
    
    def rotate(self, times) -> None: # Send the right data to Arduino (pin of the motor and rotation count)
        
        data = f'!{self.pin}/{times});'
        self.port.send(data)
        
    def __str__(self) -> str:
        return f'Motor: {self.pin}'
    
class Solver():
    
    """
        This class merges all the other models.
        The user only interacts with this class.
    """
    
    
    def __init__(self, port: str):
        self.port = Port(port) # Establish the serial communication with Arduino
        self.is_responsive = False
        self.indexes = [85, 68, 70, 66, 76, 82] # Indexes of the motors corrisponding to the letter in ASCII
        self.motors = [Motor(i, self.port) for i in range(6)]        
        self.port.connect(True) # Restart Arduino and check if it's responding

    def solve(self, cube_string: str) -> None:
        for m in koci_solve(cube_string): # For every move
            self.move(m)
        
    def move(self, cMove: list) -> None:
        """
            Processes the moves and tells the right motor to send the data to Arduino
        """
        
        times = 1
        if '\'' in cMove: # If the move contains a ' (anti-clockwise rotation or 3 rotations)
            times = 3
        elif '2' in cMove: # If the move contains a 2 (double rotation)
            times = 2
        
        m = self.motors[self.indexes.index(ord(cMove[0]))] # Get the right motor (gets the index of the Motor corresponding to the letter from the Rubik's Official Notation)
        m.rotate(times)
        
def koci_solve(cube_string: str) -> list:
    moves = solve(cube_string).split() # Split every move into an array - eg [U2, B, B']
        
    cMoves = list()
    for move in moves:
        cMoves.append(list(move)) # Split every item of the move into an array - eg [[U, 2], [B], [B, ']]
    
    return cMoves
