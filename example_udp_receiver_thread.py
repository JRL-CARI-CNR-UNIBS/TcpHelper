import socket
from signal import signal, SIGINT
from sys import exit
from threading import Thread
from collections import deque
import sys
import time
from python_udp_helper import UdpReceiverThread
stop=False

def handler(signal_received, frame):
    global stop
    stop=True




if __name__ == '__main__':
    signal(SIGINT, handler)
    if len(sys.argv) < 3:
        print("error: wrong.number of input\nCorrect usage:\npython3 example_udp_server_thread.py [HOSTNAME] [PORT]")
        sys.exit()
    nome_script, hostname, port = sys.argv

    try:
        port=int(port)
    except:
        print("port has to be a integer")
        sys.exit()

    thread1 = UdpReceiverThread("Thread#1",hostname,port)
    thread1.start()
    while True:
        if stop:
            thread1.stopThread()
            break
        if (thread1.isNewStringAvailable()):
            print("new string: "+thread1.getString())
    thread1.join()
