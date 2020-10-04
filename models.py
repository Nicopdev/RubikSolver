import serial
import kociemba # To solve the cube
import time

# COMMUNICATE WITH ARDUINO (get data)
# import serial 
# arduinoPort = serial.Serial('/dev/ttyACM0', 9600)
# while 1:
#    if(arduinoPort.inWaiting() > 0):
#       myData = arduinoPort.readline()
#       print myData

# COMMUNICATE WITH ARDUINO (send data)
# import serial
# arduinoPort = serial.Serial('/dev/ttyACM0', 9600)
# arduinoPort.write('5')

class Port():
    
    def __init__(self, port, rate=9600, timeout=1): # eg. port = '/dev/ttyACM0'
        self.port = serial.Serial(port, rate, timeout=timeout)
        time.sleep(2)
    
    def send(self, data):
        self.port.write(bytes(data, 'ascii'))
        
    def get(self):
        if self.port.inWaiting() > 0:
            return self.port.read(self.port.inWaiting())
        return ''

    def waiting(self):
        return self.port.inWaiting()
    
    def reset(self):
        self.port.setDTR(False)
        time.sleep(1)
        self.port.flushInput()
        self.port.setDTR(True)


# RED = U
# GREEN = F
# ORANGE = D
# BLUE = B
# YELLOW = R
# WHITE = L

class Koci():
    
    def solve(self, cube_string):
        moves = kociemba.solve(cube_string).split()
        
        cMoves = list()
        for move in moves:
            cMoves.append(list(move))
            
        return cMoves
    
class Motor():
    
    def __init__(self, pin, port):
        self.pin = pin
        self.port = port
    
    def rotate(self, times):
        data = "!"
        data += str(self.pin) + "/" + str(times) + ")"
        data += ";"
        
        self.port.send(data)
        
    def __str__(self):
        return 'Motor ' + str(self.pin)
    
class Solver():
    
    def __init__(self, port):
        self.port = Port(port)
        self.is_responsive = False
        self.indexes = [85, 68, 70, 66, 76, 82] # Indexes of the motors corrisponding to the letter in ASCII
        self.motors = [
                        Motor(0, self.port),
                        Motor(1, self.port),
                        Motor(2, self.port),
                        Motor(3, self.port),
                        Motor(4, self.port),
                        Motor(5, self.port),
                        ]
        
        self.connect(True)
        
    def __move__(self, cMove):
        times = 1
        if '\'' in cMove:
            times = 3
        elif '2' in cMove:
            times = 2
        
        m = self.motors[self.indexes.index(ord(cMove[0]))]
        m.rotate(times)
    
    def solve(self, cubeString):
        for m in Koci().solve(cubeString):
            self.__move__(m)
    
    def connect(self, reset):
        if reset:
            self.port.reset()
        
        while self.is_responsive == False:
            while self.port.waiting() > 0:
                if str(self.port.get().decode('ascii')) == '!':
                    self.is_responsive = True
                    print('Arduino is connected and responsive.')
                else:
                    print('Arduino is connected, but unresponsive.')
        
        
        
        
        
