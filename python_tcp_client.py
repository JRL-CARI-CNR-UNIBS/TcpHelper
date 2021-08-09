import socket

from signal import signal, SIGINT
from sys import exit
from threading import Thread

stop=False
def handler(signal_received, frame):
    global stop
    stop=True


if __name__ == '__main__':
    signal(SIGINT, handler)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 1239))

    s.settimeout(0.1)
    while True:
        full_msg = ''
        while True:
            if stop:
                break
            try:
                msg = s.recv(8)
                if len(msg) <= 0:
                    break
                full_msg += msg.decode("utf-8")
                #print("running: "+full_msg+"\n")
            except:
                break
        if len(full_msg) > 0:
            print(full_msg+"\n")
        if stop:
            break;

    s.close()
