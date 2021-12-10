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

//    std::string host_name=boost::asio::ip::host_name();
   std::string port =argv[1];
    std::cout << "port : " <<std::atoi(port.c_str())<<std::endl;

    tcp_helper::UdpReceiver string_receiver(port,stop);
    std::thread udp_thread(&tcp_helper::UdpReceiver::thread,&string_receiver);

    while (not stop)
    {
      if (string_receiver.isUnreadStringAvailable())
        std::cout << "received = " << string_receiver.getString() << std::endl;
      usleep(200000);
    }
    if (udp_thread.joinable())
      udp_thread.join();

  }
  catch (std::exception& e)
  {
    std::cerr << "Exception: " << e.what() << "\n";
  }

  return 0;
}
