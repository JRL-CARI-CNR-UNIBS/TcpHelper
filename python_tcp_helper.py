import socket
from signal import signal, SIGINT
from sys import exit
from threading import Thread
from collections import deque
import sys

global stop
class ReadStringThread (Thread):
    def __init__(self, name,hostname,port):
        Thread.__init__(self)
        self.name = name
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((hostname, port))
        print("host name "+socket.gethostname(),". port ",port)
        self.s.settimeout(0.1)
        self.new_string=False;
        self.string=""
        self.queue = deque()
        self.stop=False
    def isNewStringAvailable(self):
        return len(self.queue)>0

    def stopThread(self):
        self.stop=True

    def getString(self):
        self.new_string=False;
        #return self.string
        if len(self.queue)>0:
            return self.queue.popleft()
        else:
            return ""
    def run(self):
        while True:
            full_msg = ''
            while True:
                if self.stop:
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
                full_msg=""

            if self.stop:
                break;

        self.s.close()

class TcpServerThread (Thread):
    def __init__(self, name,hostname,port):
        Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((hostname, port))
        self.s.listen(5)
        self.queue = deque()
        self.stop=False
    def hasEmptyQueue(self):
        return len(self.queue)==0

    def stopThread(self):
        self.stop=True

    def sendString(self,string):
        self.queue.append(string)

    def run(self):

        while True:
            if self.stop:
                break;
            # now our endpoint knows about the OTHER endpoint.
            clientsocket, address = self.s.accept()
            print(f"Connection from {address} has been established.")
            while True:
                if self.stop:
                    break
                try:
                    if len(self.queue)>0:
                        string=self.queue.popleft()
                        clientsocket.send(bytes(string+"\n","utf-8"))
                except:
                    print("connection lost, waiting for a new one")
            clientsocket.close()


        self.s.close()
