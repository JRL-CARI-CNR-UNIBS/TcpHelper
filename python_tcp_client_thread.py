import socket

from signal import signal, SIGINT
from sys import exit
from threading import Thread
from collections import deque
import sys
stop=False


def handler(signal_received, frame):
    global stop
    stop=True

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
                full_msg=""

            if stop:
                break;

        self.s.close()

if __name__ == '__main__':
    signal(SIGINT, handler)
    if len(sys.argv) < 3:
        print("error: wrong.number of input\nCorrect usage:\npython3 python_tcp_client_thread.py [HOSTNAME] [PORT]")
        sys.exit()
    nome_script, hostname, port = sys.argv

    try:
        port=int(port)
    except:
        print("port has to be a integer")
        sys.exit()
    # hostname=socket.gethostname()
    # port=1239
    thread1 = ReadStringThread("Thread#1",hostname,port)
    thread1.start()
    while True:
        if stop:
            break
        if (thread1.isNewStringAvailable()):
            print("new string: "+thread1.getString())
    thread1.join()
