cmake_minimum_required(VERSION 3.5)

project(test_socket LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
SET(Boost_USE_STATIC_LIBS OFF)
SET(Boost_USE_MULTITHREAD ON)
find_package(Boost 1.40.0 REQUIRED system thread regex)

include_directories(
   ${Boost_INCLUDE_DIRS}
)
add_executable(tcp_client cpp_tcp_client.cpp)
target_link_libraries( tcp_client
 ${Boost_LIBRARIES}
)

add_executable(tcp_server cpp_tcp_server.cpp)
target_link_libraries( tcp_server
 ${Boost_LIBRARIES}
)
