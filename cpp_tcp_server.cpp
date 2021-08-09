//
// blocking_tcp_echo_server.cpp
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
// Copyright (c) 2003-2016 Christopher M. Kohlhoff (chris at kohlhoff dot com)
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//

#include <cstdlib>
#include <iostream>
#include <boost/bind.hpp>
#include <boost/smart_ptr.hpp>
#include <boost/asio.hpp>
#include <boost/thread/thread.hpp>
#include "tcp_classes.h"
#include <queue>
#include <mutex>
using boost::asio::ip::tcp;

bool stop=false;

void my_handler(int s)
{
  printf("Caught signal %d\n",s);
  stop=true;
}


int main(int argc, char* argv[])
{
  if (argc != 2)
  {
    std::cerr << "Usage: blocking_tcp_echo_server <port>\n";
    return 1;
  }

  tcp_helper::TcpServer server(std::atoi(argv[1]),stop);
  std::thread t(&tcp_helper::TcpServer::thread,&server);
  int idx=0;

  while (not stop)
  {
    std::string str="pippo_"+std::to_string(idx++)+"\n";
    server.sendString(str);
    sleep(2);
  }
  if (t.joinable())
    t.join();


  return 0;
}
