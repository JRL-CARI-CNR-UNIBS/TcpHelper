//
// blocking_tcp_echo_client.cpp
// ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
// Copyright (c) 2003-2021 Christopher M. Kohlhoff (chris at kohlhoff dot com)
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//

#include <cstdlib>
#include <cstring>
#include <iostream>
#include <boost/asio.hpp>
#include <signal.h>
#include "tcp_classes.h"
using boost::asio::ip::tcp;

enum { max_length = 1024 };
bool stop=false;

void my_handler(int s)
{
  printf("Caught signal %d\n",s);
  stop=true;
}



int main(int argc, char* argv[])
{
  signal (SIGINT,my_handler);
  try
  {
    if (argc != 2)
    {
      std::cerr << "Usage: blocking_tcp_echo_client <port>\n";
      return 1;
    }

    std::string host_name=boost::asio::ip::host_name();
    std::cout << "host name : " <<host_name<<std::endl;

    tcp_helper::TcpClient string_rec(host_name,argv[1],stop);
    std::thread tcp_thread(&tcp_helper::TcpClient::thread,&string_rec);
    if (tcp_thread.joinable())
      tcp_thread.join();

  }
  catch (std::exception& e)
  {
    std::cerr << "Exception: " << e.what() << "\n";
  }

  return 0;
}
