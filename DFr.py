import serial
import time
import collections

class slcan:
    def __init__(self, interface, buffsize=10):
        self.interface = interface
        self.buffsize = buffsize

        self.sob = serial.Serial(
            port='/dev/ttyACM'+str(interface),
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
            )
        self._write('h')
        time.sleep(1)
        self._write('S4')
        time.sleep(1)
        self.start()
        self._write('t123411223344')


        self.write_buff = collections.deque(maxlen=buffsize)
    
    def _write(self,message):
        self.sob.write(bytes(message+'\r\n','utf-8'))

    def read(self):
        print(self.sob.read(100))

    def write(self,frame):
        self.write_buff.append(frame)

    def start(self):
        self._write('O')
    
    def stop(self):
        self._write('C')


if __name__=='__main__':
    df = slcan(0)
    for i in range(10):
        df.write(i)


    df.write(213432)
    print(df.write_buff)
        
