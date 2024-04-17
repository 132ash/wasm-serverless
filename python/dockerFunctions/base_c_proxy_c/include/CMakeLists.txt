cmake_minimum_required(VERSION 3.14)
project(wasmProxy VERSION 0.1)  

add_compile_options(-pthread)

add_executable(wasmProxy wasmProxy.cpp) 

target_link_libraries (wasmProxy PUBLIC -lpthread)