cmake_minimum_required(VERSION 3.14)
project(proxy)

# C++ Standard Requirement
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Include Boost for subprocess handling and filesystem
find_package(Boost 1.65 REQUIRED COMPONENTS system filesystem)

# Set source files
set(SOURCE_FILES
proxy.cpp
)

# Include directories for httplib and nlohmann_json
include_directories(${Boost_INCLUDE_DIR})

# Add executable based on the source file
add_executable(proxy ${SOURCE_FILES})

# Link libraries to the executable
target_link_libraries(proxy
    PRIVATE
        ${Boost_LIBRARIES}
        pthread
)