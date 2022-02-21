import socket
from signal import signal, SIGINT
from sys import exit
from threading import Thread
from threading import Lock
from collections import deque
import time
import sys

global stop
class UdpReceiverThread (Thread):
    def __init__(self, name,hostname,port):
        Thread.__init__(self)
        self.name = name
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((hostname, port))
        print("host name "+socket.gethostname(),". port ",port)
        self.s.settimeout(0.1)
        self.queue = deque()
        self.stop=False
        self.lock = Lock()

    def __del__(self):
        self.stop=True
        print(self.name+": stop")
        self.s.close()

    def isNewStringAvailable(self):
        self.lock.acquire()
        flag=len(self.queue)>0
        self.lock.release()
        return flag

    def stopThread(self):
        self.stop=True
        print("stopping "+self.name)

    def getString(self):
        self.new_string=False;
        str=""
        self.lock.acquire()
        if len(self.queue)>0:
            str=self.queue.popleft()
        self.lock.release()
        return str

    def getLastStringAndClearQueue(self):
        self.new_string=False;
        str=""
        self.lock.acquire()
        if len(self.queue)>0:
            str=self.queue.pop()
            self.queue.clear()
        self.lock.release()
        return str

    def run(self):
        print("init")

        while True:

            full_msg = ''
            while True:
                time.sleep(0.01)
                if self.stop:
                    break
                try:
                    msg, addr = self.s.recvfrom(1024) # buffer size is 1024 bytes
                    full_msg += msg.decode("utf-8")
                except:
                    break
            if len(full_msg) > 0:
                self.new_string=True;
                self.string=full_msg
                self.queue.append(full_msg.strip('\n'))
                full_msg=""

            if self.stop:
                break;
        print("exit ",self.name)
        self.s.close()

class UdpSenderThread (Thread):
    def __init__(self, name,hostname,port):
        Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port=port
        self.hostname=hostname
        self.queue = deque()
        self.stop=False
        self.lock = Lock()
        self.name = name

    def __del__(self):
        print(self.name+": stop")
        self.stop=True
        self.s.close()

    def hasEmptyQueue(self):
        self.lock.acquire()
        flag=len(self.queue)==0
        self.lock.release()
        return flag

    def stopThread(self):
        self.stop=True
        print("stopping "+self.name)
    def sendString(self,string):
        self.lock.acquire()
        self.queue.append(string)
        self.lock.release()

    def run(self):
        while True:
            if self.stop:
                break;
            # now our endpoint knows about the OTHER endpoint.
            try:
                while True:
                    if self.stop:
                        break
                    self.lock.acquire()
                    #print("length "+str(len(self.queue)))
                    if len(self.queue)>0:
                        string=self.queue.popleft()
                    else:
                        self.lock.release()
                        continue
                    self.lock.release()
                    try:
                        self.s.sendto(bytes(string+"\n","utf-8"),(self.hostname,self.port))
                    except:
                        print(self.name +": connection lost, waiting for a new one")
                        self.lock.acquire()
                        self.queue.append(string)
                        self.lock.release()
                        break
            except:
                time.sleep(0.1)


        self.s.close()
        print("exit ",self.name)
