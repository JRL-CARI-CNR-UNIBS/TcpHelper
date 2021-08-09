# TcpHelper

# Table of Contents
1. [Before start](#Python)
2. [C++](#c++)

## Python
Written in Python3, it requires __socket__ library

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

## C++
Written in C++11, it requires __Boost.asio__

namespace __tcp_helper__

### TcpClient
Client for receiving strings. It runs in a separated thread, new strings are queued in FIFO order.

Usage:

- Constructor:
  * host_name: hostname of the TCP Server
  * port: port of the TCP connnection
  * stop_flag: a boolean value, the thread stops if it becomes true.

```
TcpClient::TcpClient(host_name,port,stop_flag);
```

You need to manually start the thread
```
tcp_helper::TcpClient string_rec(host_name,port,stop);
std::thread tcp_thread(&tcp_helper::TcpClient::thread,&string_rec);
```

- Check if a new string is available:
```
bool TcpClient::isUnreadStringAvailable()
```


- get received string (queued in FIFO order). Return "" if there are no strings.
```
std::string TcpClient::getString()
```


### TcpServer
Server for sending strings. It runs in a separated thread, new strings are queued in FIFO order.
Usage:

- Constructor:
  * host_name: hostname of the TCP Server
  * port: port of the TCP connnection
  * stop_flag: a boolean value, the thread stops if it becomes true.

```
TcpServer::TcpServer(host_name,port,stop_flag);
```

You need to manually start the thread
```
tcp_helper::TcpServer string_rec(host_name,port,stop);
std::thread tcp_thread(&tcp_helper::TcpClient::thread,&string_rec);
```

- Check if there are no strings in queue:
```
bool TcpServer::hasEmptyQueue()
```


- append string to the queue (queued in FIFO order).
```
void sendString(const std::string& str)
```
