# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.29

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/bin/cmake

# The command to remove a file.
RM = /usr/local/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/ash/wasm/wasm-serverless/python/dockerFunctions/base_c

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/ash/wasm/wasm-serverless/python/dockerFunctions/base_c/build

# Include any dependencies generated for this target.
include CMakeFiles/proxy.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/proxy.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/proxy.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/proxy.dir/flags.make

CMakeFiles/proxy.dir/proxy.cpp.o: CMakeFiles/proxy.dir/flags.make
CMakeFiles/proxy.dir/proxy.cpp.o: /home/ash/wasm/wasm-serverless/python/dockerFunctions/base_c/proxy.cpp
CMakeFiles/proxy.dir/proxy.cpp.o: CMakeFiles/proxy.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/home/ash/wasm/wasm-serverless/python/dockerFunctions/base_c/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/proxy.dir/proxy.cpp.o"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/proxy.dir/proxy.cpp.o -MF CMakeFiles/proxy.dir/proxy.cpp.o.d -o CMakeFiles/proxy.dir/proxy.cpp.o -c /home/ash/wasm/wasm-serverless/python/dockerFunctions/base_c/proxy.cpp

CMakeFiles/proxy.dir/proxy.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/proxy.dir/proxy.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/ash/wasm/wasm-serverless/python/dockerFunctions/base_c/proxy.cpp > CMakeFiles/proxy.dir/proxy.cpp.i

CMakeFiles/proxy.dir/proxy.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/proxy.dir/proxy.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/ash/wasm/wasm-serverless/python/dockerFunctions/base_c/proxy.cpp -o CMakeFiles/proxy.dir/proxy.cpp.s

# Object files for target proxy
proxy_OBJECTS = \
"CMakeFiles/proxy.dir/proxy.cpp.o"

# External object files for target proxy
proxy_EXTERNAL_OBJECTS =

proxy: CMakeFiles/proxy.dir/proxy.cpp.o
proxy: CMakeFiles/proxy.dir/build.make
proxy: /usr/lib/x86_64-linux-gnu/libboost_system.so.1.71.0
proxy: /usr/lib/x86_64-linux-gnu/libboost_filesystem.so.1.71.0
proxy: CMakeFiles/proxy.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --bold --progress-dir=/home/ash/wasm/wasm-serverless/python/dockerFunctions/base_c/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable proxy"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/proxy.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/proxy.dir/build: proxy
.PHONY : CMakeFiles/proxy.dir/build

CMakeFiles/proxy.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/proxy.dir/cmake_clean.cmake
.PHONY : CMakeFiles/proxy.dir/clean

CMakeFiles/proxy.dir/depend:
	cd /home/ash/wasm/wasm-serverless/python/dockerFunctions/base_c/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/ash/wasm/wasm-serverless/python/dockerFunctions/base_c /home/ash/wasm/wasm-serverless/python/dockerFunctions/base_c /home/ash/wasm/wasm-serverless/python/dockerFunctions/base_c/build /home/ash/wasm/wasm-serverless/python/dockerFunctions/base_c/build /home/ash/wasm/wasm-serverless/python/dockerFunctions/base_c/build/CMakeFiles/proxy.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : CMakeFiles/proxy.dir/depend

