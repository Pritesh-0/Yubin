import socket


host,port='localhost',9090
sock = socket.socket()

sock.connect((host,port))


data=sock.recv(1024).decode()
print(data)
sock.close()
