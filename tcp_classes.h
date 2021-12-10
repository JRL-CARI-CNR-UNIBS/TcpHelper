#pragma once
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <boost/asio.hpp>
#include <queue>
#include <mutex>
using boost::asio::ip::tcp;
using boost::asio::ip::udp;

namespace tcp_helper
{

typedef std::shared_ptr<tcp::socket> socket_ptr;
typedef std::shared_ptr<udp::socket> udp_socket_ptr;
inline std::string make_string(boost::asio::streambuf& streambuf)
{
 return {buffers_begin(streambuf.data()),
         buffers_end(streambuf.data())};
}

class TcpClient
{
protected:
  boost::asio::io_context io_context;
  tcp::socket s;
  tcp::resolver resolver;
  bool& stop_;
  std::queue<std::string> queue_;
  std::mutex mtx;


  std::string read()
  {
    boost::asio::streambuf b;
    try {
      boost::asio::read_until(s, b, '\n');
    }
    catch (...)
    {

    }

    std::string str=make_string(b);
    if (str.size()>0)
    {
      mtx.lock();
      queue_.push(str);
      mtx.unlock();
    }
    return str;
  }

public:
  TcpClient(std::string hostname, std::string port, bool& stop_flag):
    s(io_context),
    resolver(io_context),
    stop_(stop_flag)
  {
    boost::asio::connect(s, resolver.resolve(hostname, port));
  };

  bool isUnreadStringAvailable()
  {
    return  (not queue_.empty());
  }

  std::string getString()
  {
    std::string str="";
    mtx.lock();
    if (queue_.size()>0)
    {
      str=queue_.front();
      queue_.pop();
    }
    return str;
  }

  void thread()
  {
    while (not stop_)
    {
      read();
      usleep(1000);
    }
  }
};


class TcpServer
{
protected:
  boost::asio::io_service io_service;
  tcp::acceptor a;
  socket_ptr sock;
  bool& stop_;
  std::queue<std::string> queue;
  std::mutex mtx;
public:
  TcpServer(int port, bool& stop_flag):
    a(io_service, tcp::endpoint(tcp::v4(), port)),
    stop_(stop_flag)
  {
    sock=std::make_shared<tcp::socket>(io_service);
  }

  void sendString(const std::string& str)
  {
    mtx.lock();
    queue.push(str);
    mtx.unlock();
  }

  bool hasEmptyQueue()
  {
    return queue.empty();
  }

  void thread()
  {
    a.accept(*sock);
    while (not stop_)
    {
      mtx.lock();
      if (not queue.empty())
      {
        std::string str=queue.front();
        queue.pop();
        mtx.unlock();
        try
        {
          boost::asio::write(*sock, boost::asio::buffer(str, str.length()));
        }
        catch (std::exception& e)
        {
          std::cerr << "Exception in thread: " << e.what() << "\n";
          sock=std::make_shared<tcp::socket>(io_service);
          a.accept(*sock);
        }
      }
      else
        mtx.unlock();

      usleep(1e4);
    }
  }
};

class UdpSender
{
protected:
  boost::asio::io_service io_service;
  boost::asio::io_context io_context;
  udp::endpoint remote_endpoint;
  udp::resolver resolver;
  udp_socket_ptr sock;
  std::string hostname_;
  std::string port_;
  bool& stop_;
  std::queue<std::string> queue;
  std::mutex mtx;
public:
  UdpSender(std::string hostname, std::string port, bool& stop_flag):
    hostname_(hostname),
    resolver(io_context),
    port_(port),
    stop_(stop_flag)
  {
    boost::system::error_code error;
    udp::resolver::iterator iter = resolver.resolve(hostname, port,error);
    assert(!error);
    remote_endpoint = *iter;

    sock=std::make_shared<udp::socket>(io_service, udp::endpoint(udp::v4(), 0));

  }

  void sendString(const std::string& str)
  {
    mtx.lock();
    queue.push(str);
    mtx.unlock();
  }

  bool hasEmptyQueue()
  {
    return queue.empty();
  }

  void thread()
  {
    boost::system::error_code err;
    while (not stop_)
    {
      mtx.lock();
      if (not queue.empty())
      {
        std::string str=queue.front();
        queue.pop();
        mtx.unlock();
        try
        {
          std::cout << "send " << str << std::endl;

          auto sent = sock->send_to(boost::asio::buffer(str,str.size()), remote_endpoint, 0, err);
          std::cout << "error code = " << err << std::endl;
        }
        catch (std::exception& e)
        {
          //remote_endpoint = udp::endpoint(boost::asio::ip::address::from_string(hostname_), port_);

          std::cerr << "Exception in thread: " << e.what() << "\n";
        }
      }
      else
        mtx.unlock();

      usleep(1e4);
    }
  }
};

class UdpReceiver
{
protected:
  boost::asio::io_service io_service;
  boost::asio::io_context io_context;
  udp::endpoint remote_endpoint;
  udp::resolver resolver;
  udp_socket_ptr sock;
  std::string port_;
  bool& stop_;
  std::queue<std::string> queue_;
  std::mutex mtx;


  std::string read()
  {
    char buffer[1024]={};
    udp::endpoint ep_sender;
    std::string str="";
    while (true)
    {
      std::size_t received_char=sock->receive_from(boost::asio::buffer(buffer), ep_sender);
      if (stop_)
        break;
      if (received_char<=0)
        break;
      str.clear();
      str=std::string(buffer, received_char);
      mtx.lock();
      queue_.push(str);
      mtx.unlock();
    }
    return str;
  }


public:
  UdpReceiver(std::string port, bool& stop_flag):
    resolver(io_context),
    port_(port),
    stop_(stop_flag)
  {
    boost::system::error_code error;
    int port_int=std::stoi(port);
    assert(!error);
    remote_endpoint = udp::endpoint(boost::asio::ip::address_v4::any(), port_int);

    sock=std::make_shared<udp::socket>(io_context, udp::endpoint(udp::v4(), port_int));
  }

  bool isUnreadStringAvailable()
  {
    return  (not queue_.empty());
  }

  std::string getString()
  {
    std::string str="";
    mtx.lock();
    if (queue_.size()>0)
    {
      str=queue_.front();
      queue_.pop();
    }
    return str;
  }

  void thread()
  {
    while (not stop_)
    {
      read();
      usleep(1000);
    }
  }

};

}

