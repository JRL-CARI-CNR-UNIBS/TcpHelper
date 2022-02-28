import socket
from signal import signal, SIGINT
from sys import exit
from threading import Thread
from collections import deque
import sys
import time
from python_binary_udp_helper import UdpBinarySenderThread
stop=False

def handler(signal_received, frame):
    global stop
    stop=True




if __name__ == '__main__':
    signal(SIGINT, handler)
    if len(sys.argv) < 3:
        print("error: wrong.number of input\nCorrect usage:\npython3 example_tcp_server.py [HOSTNAME] [PORT]")
        sys.exit()
    nome_script, hostname, port = sys.argv

    try:
        port=int(port)
    except:
        print("port has to be a integer")
        sys.exit()

    thread1 = UdpBinarySenderThread("Thread#1",hostname,port)
    idx=0
    t0=time.time()
    while True:
        if stop:
            break

        data=[time.time()]
        thread1.sendData(data)
        idx+=1
        time.sleep(0.001)
