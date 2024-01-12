import pygame

def conv(v):

    v=int(v*10000)
    vs=float(v-(10000))/float(20000)
    val = 19200000 + int(vs*8000000)
    return val


def startJoy():
    pygame.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    #while True:
        #pygame.event.get()
        #joystick=joysticks[0]
    #print(joystick.get_numaxes())
        #b1,b2,b3 = joystick.get_axis(0),joystick.get_axis(1),joystick.get_axis(4)
    #print("b1: ",conv(b1)) 
    #print("b2: ",conv(b2))
    #print("b3: ",conv(b3))


        #time.sleep(0.1)

    #msgid=768
    #ctype=10
    #num=10
        #msg=conv(b1)
        #sob.write()
        #msg='{},{},{},{}\r\n'.format(msgid,ctype,conv(b1),num)
        #sob.write(bytes(msg, 'utf-8'))
        #msg='{},{},{},{}\r\n'.format(msgid,ctype,conv(b2),num)
        #sob.write(bytes(msg, 'utf-8'))
        #msg='{},{},{},{}\r\n'.format(msgid,ctype,conv(b3),num)
        #sob.write(bytes(msg, 'utf-8'))

    #print(msg)

#if __name__ == '__main__'


