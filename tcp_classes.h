#include <cstdlib>
#include <cstring>
#include <iostream>
#include <boost/asio.hpp>
#include <queue>
#include <mutex>
using boost::asio::ip::tcp;

namespace tcp_helper
{

typedef std::shared_ptr<tcp::socket> socket_ptr;
std::string make_string(boost::asio::streambuf& streambuf)
{
 return {buffers_begin(streambuf.data()),
         buffers_end(streambuf.data())};
}

class TcpClient
{
public:
  boost::asio::io_context io_context;
  tcp::socket s;
  tcp::resolver resolver;
  bool& stop_;
  bool new_string=false;
  std::queue<std::string> queue_;
  std::mutex mtx;
  TcpClient(std::string hostname, std::string port, bool& stop_flag):
    s(io_context),
    resolver(io_context),
    stop_(stop_flag)
  {
    boost::asio::connect(s, resolver.resolve(hostname, port));
  };

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
      new_string=true;
      queue_.push(str);
      mtx.unlock();
      std::cout << str << std::endl;
    }
    return str;
  }

  bool isUnreadStringAvailable()
  {
    return  (not queue_.empty());
  }

  std::string getString()
  {
    std::string str=queue_.front();
    queue_.pop();
    return str;
  }

  void thread()
  {
    while (not stop_)
    {
      read();
      usleep(10000);
    }
  }
};


class TcpServer
{
public:
  boost::asio::io_service io_service;
  tcp::acceptor a;
  socket_ptr sock;
  bool& stop_;
  std::queue<std::string> queue;
  std::mutex mtx;
  TcpServer(int port, bool& stop_flag):
    a(io_service, tcp::endpoint(tcp::v4(), port)),
    stop_(stop_flag)
  {
    sock=std::make_shared<tcp::socket>(io_service);
    a.accept(*sock);
  }

  void sendString(const std::string str)
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

      usleep(1000000);

    }
  }
};
}

