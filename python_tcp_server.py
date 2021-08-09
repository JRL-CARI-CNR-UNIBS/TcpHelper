import socket
from signal import signal, SIGINT
from sys import exit
from threading import Thread
from collections import deque
import sys
import time
stop=False
def handler(signal_received, frame):
    global stop
    stop=True


class TcpServerThread (Thread):
    def __init__(self, name,hostname,port):
        Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((hostname, port))
        self.s.listen(5)
        self.queue = deque()
    def hasEmptyQueue(self):
        return len(self.queue)==0
    def sendString(self,string):
        self.queue.append(string)
    def run(self):
        global stop
        while True:
            if stop:
                break;
            # now our endpoint knows about the OTHER endpoint.
            clientsocket, address = self.s.accept()
            print(f"Connection from {address} has been established.")
            while True:
                if stop:
                    break
                try:
                    print("in queue = ",len(self.queue))
                    if len(self.queue)>0:
                        string=self.queue.popleft()
                        clientsocket.send(bytes(string+"\n","utf-8"))
                        print("sent")
                except:
                    print("connection lost, waiting for a new one")
            clientsocket.close()


        self.s.close()

if __name__ == '__main__':
    signal(SIGINT, handler)
    if len(sys.argv) < 3:
        print("error: wrong.number of input\nCorrect usage:\npython3 python_tcp_server.py [HOSTNAME] [PORT]")
        sys.exit()
    nome_script, hostname, port = sys.argv

    try:
        port=int(port)
    except:
        print("port has to be a integer")
        sys.exit()
    # hostname=socket.gethostname()
    # port=1239
    thread1 = TcpServerThread("Thread#1",hostname,port)
    thread1.start()
    while True:
        if stop:
            break
        thread1.sendString("pippo")
        time.sleep(1)
    thread1.join()
