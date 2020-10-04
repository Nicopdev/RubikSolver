from serial import Serial
from kociemba import solve # To solve the cube
from time import sleep

class Port:
    def __init__(self, port, rate=9600, timeout=1): # eg. port = '/dev/ttyACM0'
        self.port = Serial(port, rate, timeout=timeout)
        sleep(2)
    
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
    
class Motor:
    def __init__(self, pin, port):
        self.pin = pin
        self.port = port
    
    def rotate(self, times) -> None:
        data = f'!{self.pin}/{times});'
        self.port.send(data)
        
    def __str__(self) -> str:
        return f'Motor: {self.pin}'
    
class Solver:
    def __init__(self, port):
        self.port = Port(port)
        self.is_responsive = False
        self.indexes = [85, 68, 70, 66, 76, 82] # Indexes of the motors corrisponding to the letter in ASCII
        self.motors = [Motor(i, self.port) for i in range(6)]
        
        self.connect(True)
        
    def move(self, cMove):
        times = 1
        if '\'' in cMove:
            times = 3
        elif '2' in cMove:
            times = 2
        
        m = self.motors[self.indexes.index(ord(cMove[0]))]
        m.rotate(times)
    
    def solve(self, cubeString: str) -> None:
        for m in koci_solve(cubeString):
            self.move(m)
    
    def connect(self, reset: bool) -> None:
        if reset:
            self.port.reset()
        
        while not self.is_responsive:
            while self.port.waiting():
                if self.port.get().decode('ascii') == '!':
                    self.is_responsive = True
                    print('Arduino is connected and responsive.')
                else:
                    print('Arduino is connected, but unresponsive.')
        
def koci_solve(cube_string: str) -> list:
    moves = solve(cube_string).split()
    
    cMoves = []
    for move in moves:
        cMoves.append([move])
        
    return cMoves