from models import Solver

solver = Solver('/dev/cu.usbmodem14101')
solver.solve('DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD')

def main():
    result = ''
    while 1:
        while solver.port.waiting():
            result += solver.port.get().decode('ascii')
            print(result.replace('\n', ' '))

if __name__ == '__main__':
    main()