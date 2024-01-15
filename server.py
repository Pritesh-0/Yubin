import socket
import json
host,port='localhost',9090

m={"a":1,"b":2}

data = json.dumps(m)

sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sock.bind((host,port))

sock.listen(5)

while True:
    c,addr=sock.accept()

    c.send(data.encode())

    #c.close()
    #break
