cmake_minimum_required(VERSION 3.14)
project(cppExample VERSION 0.1)  

add_compile_options(-pthread)

add_executable(cppExample testWorker.cpp) 
