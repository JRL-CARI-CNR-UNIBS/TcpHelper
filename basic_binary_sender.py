import socket
import struct

ip="localhost"
port=21011
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = socket.gethostname()  # Get the local machine name
s.connect((ip, port))

status=[0,-1.0]
try:
    tmp=struct.pack(f'{len(status)}d', *status)
except:
    disp(status)
try:
    s.send(tmp)
except:
    disp(tmp)
s.close()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = socket.gethostname()  # Get the local machine name
s.connect((ip, port))
status=[1,1.0]
s.send(struct.pack(f'{len(status)}d', *status))
