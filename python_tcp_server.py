import socket
import time
from signal import signal, SIGINT
from sys import exit

stop=False
def handler(signal_received, frame):
    global stop
    stop=True

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 1239))
    s.listen(5)
    time.sleep(0.1)
    while True:
        if stop:
            break;
        # now our endpoint knows about the OTHER endpoint.
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established.")
        try:
            for i in range(0,10):
                clientsocket.send(bytes("Hey there!!!"+"\n","utf-8"))
                time.sleep(1.1)
                print("sent")
            clientsocket.close()
        except:
            print("connection lost, waiting for a new one")
