# TcpHelper

## Python

### _TcpClientThread_:
Client for receiving strings. It runs in a separated thread, new strings are queued in FIFO order.

Usage:

- Constructor:
  * server_name: name of the server, used for logging and debugging
  * host_name: hostname of the TCP Server
  * port: port of the TCP connnection

```
thread1 = TcpClientThread(server_name,host_name,port)
```

- Start Server
```
thread1.start()
```

- Check if a new string is available:
```
thread1.isNewStringAvailable()
```

- stop TCP Server:
```
thread1.stopThread()
```

- get received string (queued in FIFO order). Return "" if there are no strings.
```
thread1.getString()
```

### _TcpServerThread_:
Server for sending strings. It runs in a separated thread, new strings are queued in FIFO order.

Usage:

- Constructor:
  * server_name: name of the server, used for logging and debugging
  * host_name: hostname of the TCP server
  * port: port of the TCP connnection

```
thread1 = TcpServerThread(server_name,host_name,port)
```

- Start Server
```
thread1.start()
```

- Check if there are no strings in queue:
```
thread1.hasEmptyQueue()
```

- stop TCP Server:
```
thread1.stopThread()
```

- append string to the queue (queued in FIFO order).
```
thread1.sendString(string)
```


### Examples
```
python3 example_tcp_server.py HOSTNAME PORT
```
```
python3 example_tcp_client.py HOSTNAME PORT
```
