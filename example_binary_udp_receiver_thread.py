import socket
from signal import signal, SIGINT
from sys import exit
from threading import Thread
from collections import deque
import sys
import time
from python_binary_udp_helper import UdpBinaryReceiverThread
stop=False

def handler(signal_received, frame):
    global stop
    stop=True




if __name__ == '__main__':
    signal(SIGINT, handler)
    if len(sys.argv) < 4:
        print("error: wrong.number of input\nCorrect usage:\npython3 example_udp_server_thread.py [HOSTNAME] [PORT] [SIZE]")
        sys.exit()
    nome_script, hostname, port,size = sys.argv


    try:
        port=int(port)
    except:
        print("port has to be a integer")
        sys.exit()

    thread1 = UdpBinaryReceiverThread("Thread#1",hostname,port)
    thread1.bufferLength(int(size))
    thread1.start()
    while True:
        if stop:
            thread1.stopThread()
            break
        if (thread1.isNewDataAvailable()):
            data=thread1.getData()
            print(data)
            #if ((time.time()-data[0])>0.002):
            #    print("new data: ",(time.time()-data[0])*1e3,' ms')
        time.sleep(0.001)
    thread1.join()
