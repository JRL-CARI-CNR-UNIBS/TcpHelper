import socket
import time
UDP_IP = "127.0.0.1"
#UDP_IP = "dusseldorf"
UDP_PORT = 5005
MESSAGE = b"Hello, World!"

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
for i in range(0,10):
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    time.sleep(1)
