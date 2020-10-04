from models import Solver


solver = Solver('/dev/cu.usbmodem14101')
solver.solve('DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD')

result = ''
while 1:
    while solver.port.waiting():
        result += solver.port.get().decode('ascii')
        print(result.replace('\n', ' '))