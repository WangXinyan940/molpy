cmake_minimum_required(VERSION 3.20)

project(molpy_cpp)
set(CMAKE_CXX_STANDARD 11)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -Wall")

set(SRC_DIR src)
set(INCLUDE_DIR include)
include_directories(${INCLUDE_DIR})

add_library(randomWalk STATIC ${SRC_DIR}/simpleRW.cpp)

find_package(pybind11)
pybind11_add_module(
    molpy_cpp
    molpy_bind.cpp
)
target_link_libraries(molpy_cpp PRIVATE randomWalk)

