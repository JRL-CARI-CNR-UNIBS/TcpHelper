import socket

from signal import signal, SIGINT
from sys import exit
from threading import Thread
from collections import deque

stop=False


def handler(signal_received, frame):
    global stop
    stop=True

class ReadStringThread (Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((socket.gethostname(), 1239))
        print("host name "+socket.gethostname())
        self.s.settimeout(0.1)
        self.new_string=False;
        self.string=""
        self.queue = deque()
    def isNewStringAvailable(self):
        return len(self.queue)>0
    def getString(self):
        self.new_string=False;
        #return self.string
        if len(self.queue)>0:
            return self.queue.popleft()
        else:
            return ""
    def run(self):
        global stop
        print ("Thread '" + self.name + "' avviato")
        while True:
            full_msg = ''
            while True:
                if stop:
                    break
                try:
                    msg = self.s.recv(8)
                    if len(msg) <= 0:
                        break
                    full_msg += msg.decode("utf-8")
                    #print("running: "+full_msg+"\n")
                except:
                    break
            if len(full_msg) > 0:
                self.new_string=True;
                self.string=full_msg
                self.queue.append(full_msg)
                print(full_msg+"\n")
                full_msg=""

            if stop:
                break;

        self.s.close()
        print ("Thread '" + self.name + "' terminato")

if __name__ == '__main__':
    signal(SIGINT, handler)
    thread1 = ReadStringThread("Thread#1")
    thread1.start()
    while True:
        if stop:
            break
        if (thread1.isNewStringAvailable()):
            print("new string: "+thread1.getString())
    thread1.join()
