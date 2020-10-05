# -*- coding: utf-8 -*-

from models import Solver

solver = Solver('/dev/cu.usbmodem14101')
solver.solve('DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD') # This string represents the scrumbled cube (see https://pypi.org/project/kociemba/)

def main():
    
    # Get a feedback since no hardware is currently connected to the Arduino
    result = ''
    while True:
        while solver.port.waiting():
            result += solver.port.get().decode('ascii')
            print(result.replace('\n', ''))
            
if __name__ == '__main__':
    main()
