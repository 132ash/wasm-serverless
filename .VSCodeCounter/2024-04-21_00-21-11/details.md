# Details

Date : 2024-04-21 00:21:11

Directory /home/ash/wasm/wasm-serverless/python

Total : 180 files,  40542 codes, 5359 comments, 6413 blanks, all 52314 lines

[Summary](results.md) / Details / [Diff Summary](diff.md) / [Diff Details](diff-details.md)

## Files
| filename | language | code | comment | blank | total |
| :--- | :--- | ---: | ---: | ---: | ---: |
| [python/config/config.py](/python/config/config.py) | Python | 18 | 7 | 6 | 31 |
| [python/config/workerNodeInfo.yaml](/python/config/workerNodeInfo.yaml) | YAML | 5 | 6 | 2 | 13 |
| [python/dockerFunctions/base/Dockerfile](/python/dockerFunctions/base/Dockerfile) | Docker | 12 | 11 | 9 | 32 |
| [python/dockerFunctions/base/container_config.py](/python/dockerFunctions/base/container_config.py) | Python | 1 | 0 | 1 | 2 |
| [python/dockerFunctions/base/image_setup.sh](/python/dockerFunctions/base/image_setup.sh) | Shell Script | 1 | 0 | 0 | 1 |
| [python/dockerFunctions/base/main.py](/python/dockerFunctions/base/main.py) | Python | 8 | 0 | 2 | 10 |
| [python/dockerFunctions/base/pip.conf](/python/dockerFunctions/base/pip.conf) | Properties | 2 | 0 | 0 | 2 |
| [python/dockerFunctions/base/proxy.py](/python/dockerFunctions/base/proxy.py) | Python | 56 | 5 | 24 | 85 |
| [python/dockerFunctions/base_c/Dockerfile](/python/dockerFunctions/base_c/Dockerfile) | Docker | 11 | 11 | 8 | 30 |
| [python/dockerFunctions/base_c/container_config.py](/python/dockerFunctions/base_c/container_config.py) | Python | 1 | 0 | 0 | 1 |
| [python/dockerFunctions/base_c/image_setup.sh](/python/dockerFunctions/base_c/image_setup.sh) | Shell Script | 1 | 0 | 0 | 1 |
| [python/dockerFunctions/base_c/pip.conf](/python/dockerFunctions/base_c/pip.conf) | Properties | 2 | 0 | 0 | 2 |
| [python/dockerFunctions/base_c/proxy.py](/python/dockerFunctions/base_c/proxy.py) | Python | 63 | 4 | 18 | 85 |
| [python/dockerFunctions/base_c_proxy_c/Dockerfile](/python/dockerFunctions/base_c_proxy_c/Dockerfile) | Docker | 6 | 6 | 7 | 19 |
| [python/dockerFunctions/base_c_proxy_c/build/CMakeCache.txt](/python/dockerFunctions/base_c_proxy_c/build/CMakeCache.txt) | CMake Cache | 342 | 0 | 78 | 420 |
| [python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/3.29.0-rc1/CMakeCCompiler.cmake](/python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/3.29.0-rc1/CMakeCCompiler.cmake) | CMake | 63 | 0 | 18 | 81 |
| [python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/3.29.0-rc1/CMakeCXXCompiler.cmake](/python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/3.29.0-rc1/CMakeCXXCompiler.cmake) | CMake | 72 | 0 | 20 | 92 |
| [python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/3.29.0-rc1/CMakeSystem.cmake](/python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/3.29.0-rc1/CMakeSystem.cmake) | CMake | 10 | 0 | 6 | 16 |
| [python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/3.29.0-rc1/CompilerIdC/CMakeCCompilerId.c](/python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/3.29.0-rc1/CompilerIdC/CMakeCCompilerId.c) | C | 682 | 61 | 153 | 896 |
| [python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/3.29.0-rc1/CompilerIdCXX/CMakeCXXCompilerId.cpp](/python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/3.29.0-rc1/CompilerIdCXX/CMakeCXXCompilerId.cpp) | C++ | 667 | 62 | 150 | 879 |
| [python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/CMakeConfigureLog.yaml](/python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/CMakeConfigureLog.yaml) | YAML | 540 | 4 | 28 | 572 |
| [python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/CMakeDirectoryInformation.cmake](/python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/CMakeDirectoryInformation.cmake) | CMake | 12 | 0 | 5 | 17 |
| [python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/Makefile.cmake](/python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/Makefile.cmake) | CMake | 59 | 0 | 6 | 65 |
| [python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/proxy.dir/DependInfo.cmake](/python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/proxy.dir/DependInfo.cmake) | CMake | 17 | 0 | 7 | 24 |
| [python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/proxy.dir/cmake_clean.cmake](/python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/proxy.dir/cmake_clean.cmake) | CMake | 10 | 0 | 2 | 12 |
| [python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/proxy.dir/compiler_depend.ts](/python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/proxy.dir/compiler_depend.ts) | TypeScript | 2 | 0 | 1 | 3 |
| [python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/server.dir/DependInfo.cmake](/python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/server.dir/DependInfo.cmake) | CMake | 17 | 0 | 7 | 24 |
| [python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/server.dir/cmake_clean.cmake](/python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/server.dir/cmake_clean.cmake) | CMake | 10 | 0 | 2 | 12 |
| [python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/server.dir/compiler_depend.ts](/python/dockerFunctions/base_c_proxy_c/build/CMakeFiles/server.dir/compiler_depend.ts) | TypeScript | 2 | 0 | 1 | 3 |
| [python/dockerFunctions/base_c_proxy_c/build/Makefile](/python/dockerFunctions/base_c_proxy_c/build/Makefile) | Makefile | 87 | 48 | 47 | 182 |
| [python/dockerFunctions/base_c_proxy_c/build/cmake_install.cmake](/python/dockerFunctions/base_c_proxy_c/build/cmake_install.cmake) | CMake | 46 | 0 | 9 | 55 |
| [python/dockerFunctions/base_c_proxy_c/image_setup.sh](/python/dockerFunctions/base_c_proxy_c/image_setup.sh) | Shell Script | 1 | 0 | 0 | 1 |
| [python/dockerFunctions/base_c_proxy_c/include/httplib.h](/python/dockerFunctions/base_c_proxy_c/include/httplib.h) | C++ | 7,651 | 326 | 1,507 | 9,484 |
| [python/dockerFunctions/base_c_proxy_c/include/json.hpp](/python/dockerFunctions/base_c_proxy_c/include/json.hpp) | C++ | 17,453 | 4,342 | 2,972 | 24,767 |
| [python/dockerFunctions/base_c_proxy_c/proxy.cpp](/python/dockerFunctions/base_c_proxy_c/proxy.cpp) | C++ | 86 | 0 | 14 | 100 |
| [python/dockerFunctions/docker_setup.sh](/python/dockerFunctions/docker_setup.sh) | Shell Script | 12 | 0 | 1 | 13 |
| [python/dockerFunctions/functions/binarytree/Dockerfile](/python/dockerFunctions/functions/binarytree/Dockerfile) | Docker | 2 | 0 | 0 | 2 |
| [python/dockerFunctions/functions/binarytree/cfile/main.c](/python/dockerFunctions/functions/binarytree/cfile/main.c) | C | 85 | 1 | 30 | 116 |
| [python/dockerFunctions/functions/binarytree/create_img.sh](/python/dockerFunctions/functions/binarytree/create_img.sh) | Shell Script | 1 | 0 | 0 | 1 |
| [python/dockerFunctions/functions/binarytree_py/Dockerfile](/python/dockerFunctions/functions/binarytree_py/Dockerfile) | Docker | 2 | 0 | 0 | 2 |
| [python/dockerFunctions/functions/binarytree_py/create_img.sh](/python/dockerFunctions/functions/binarytree_py/create_img.sh) | Shell Script | 1 | 0 | 0 | 1 |
| [python/dockerFunctions/functions/binarytree_py/main.py](/python/dockerFunctions/functions/binarytree_py/main.py) | Python | 42 | 0 | 11 | 53 |
| [python/dockerFunctions/functions/cal/Dockerfile](/python/dockerFunctions/functions/cal/Dockerfile) | Docker | 2 | 0 | 0 | 2 |
| [python/dockerFunctions/functions/cal/create_img.sh](/python/dockerFunctions/functions/cal/create_img.sh) | Shell Script | 1 | 0 | 0 | 1 |
| [python/dockerFunctions/functions/cal/main.py](/python/dockerFunctions/functions/cal/main.py) | Python | 3 | 0 | 2 | 5 |
| [python/dockerFunctions/functions/count/Dockerfile](/python/dockerFunctions/functions/count/Dockerfile) | Docker | 2 | 0 | 0 | 2 |
| [python/dockerFunctions/functions/count/create_img.sh](/python/dockerFunctions/functions/count/create_img.sh) | Shell Script | 1 | 0 | 0 | 1 |
| [python/dockerFunctions/functions/count/main.py](/python/dockerFunctions/functions/count/main.py) | Python | 12 | 0 | 3 | 15 |
| [python/dockerFunctions/functions/cut/Dockerfile](/python/dockerFunctions/functions/cut/Dockerfile) | Docker | 2 | 0 | 0 | 2 |
| [python/dockerFunctions/functions/cut/create_img.sh](/python/dockerFunctions/functions/cut/create_img.sh) | Shell Script | 1 | 0 | 0 | 1 |
| [python/dockerFunctions/functions/cut/main.py](/python/dockerFunctions/functions/cut/main.py) | Python | 23 | 2 | 10 | 35 |
| [python/dockerFunctions/functions/divide2/Dockerfile](/python/dockerFunctions/functions/divide2/Dockerfile) | Docker | 2 | 0 | 0 | 2 |
| [python/dockerFunctions/functions/divide2/create_img.sh](/python/dockerFunctions/functions/divide2/create_img.sh) | Shell Script | 1 | 0 | 0 | 1 |
| [python/dockerFunctions/functions/divide2/main.py](/python/dockerFunctions/functions/divide2/main.py) | Python | 3 | 0 | 2 | 5 |
| [python/dockerFunctions/functions/exec.py](/python/dockerFunctions/functions/exec.py) | Python | 10 | 2 | 7 | 19 |
| [python/dockerFunctions/functions/main.py](/python/dockerFunctions/functions/main.py) | Python | 6 | 0 | 2 | 8 |
| [python/dockerFunctions/functions/matmul/Dockerfile](/python/dockerFunctions/functions/matmul/Dockerfile) | Docker | 3 | 0 | 0 | 3 |
| [python/dockerFunctions/functions/matmul/create_img.sh](/python/dockerFunctions/functions/matmul/create_img.sh) | Shell Script | 1 | 0 | 1 | 2 |
| [python/dockerFunctions/functions/matmul/main.py](/python/dockerFunctions/functions/matmul/main.py) | Python | 11 | 0 | 4 | 15 |
| [python/dockerFunctions/functions/merge/Dockerfile](/python/dockerFunctions/functions/merge/Dockerfile) | Docker | 2 | 0 | 0 | 2 |
| [python/dockerFunctions/functions/merge/create_img.sh](/python/dockerFunctions/functions/merge/create_img.sh) | Shell Script | 1 | 0 | 0 | 1 |
| [python/dockerFunctions/functions/merge/main.py](/python/dockerFunctions/functions/merge/main.py) | Python | 16 | 0 | 8 | 24 |
| [python/dockerFunctions/functions/prime/Dockerfile](/python/dockerFunctions/functions/prime/Dockerfile) | Docker | 2 | 0 | 0 | 2 |
| [python/dockerFunctions/functions/prime/create_img.sh](/python/dockerFunctions/functions/prime/create_img.sh) | Shell Script | 1 | 0 | 0 | 1 |
| [python/dockerFunctions/functions/prime/main.py](/python/dockerFunctions/functions/prime/main.py) | Python | 10 | 0 | 2 | 12 |
| [python/dockerFunctions/functions/reverse/Dockerfile](/python/dockerFunctions/functions/reverse/Dockerfile) | Docker | 2 | 0 | 0 | 2 |
| [python/dockerFunctions/functions/reverse/create_img.sh](/python/dockerFunctions/functions/reverse/create_img.sh) | Shell Script | 1 | 0 | 0 | 1 |
| [python/dockerFunctions/functions/reverse/main.py](/python/dockerFunctions/functions/reverse/main.py) | Python | 3 | 0 | 2 | 5 |
| [python/dockerFunctions/functions/simple_func/Dockerfile](/python/dockerFunctions/functions/simple_func/Dockerfile) | Docker | 2 | 0 | 0 | 2 |
| [python/dockerFunctions/functions/simple_func/create_img.sh](/python/dockerFunctions/functions/simple_func/create_img.sh) | Shell Script | 1 | 0 | 0 | 1 |
| [python/dockerFunctions/functions/simple_func/main.py](/python/dockerFunctions/functions/simple_func/main.py) | Python | 6 | 0 | 2 | 8 |
| [python/dockerFunctions/functions/sleep/Dockerfile](/python/dockerFunctions/functions/sleep/Dockerfile) | Docker | 2 | 0 | 0 | 2 |
| [python/dockerFunctions/functions/sleep/create_img.sh](/python/dockerFunctions/functions/sleep/create_img.sh) | Shell Script | 1 | 0 | 0 | 1 |
| [python/dockerFunctions/functions/sleep/main.py](/python/dockerFunctions/functions/sleep/main.py) | Python | 4 | 0 | 2 | 6 |
| [python/dockerFunctions/functions/spectral_norm/Dockerfile](/python/dockerFunctions/functions/spectral_norm/Dockerfile) | Docker | 2 | 0 | 0 | 2 |
| [python/dockerFunctions/functions/spectral_norm/cfile/main.c](/python/dockerFunctions/functions/spectral_norm/cfile/main.c) | C | 65 | 1 | 9 | 75 |
| [python/dockerFunctions/functions/spectral_norm/create_img.sh](/python/dockerFunctions/functions/spectral_norm/create_img.sh) | Shell Script | 1 | 0 | 0 | 1 |
| [python/dockerFunctions/functions/spectral_norm/main.py](/python/dockerFunctions/functions/spectral_norm/main.py) | Python | 19 | 0 | 7 | 26 |
| [python/dockerFunctions/functions/spectral_norm_py/Dockerfile](/python/dockerFunctions/functions/spectral_norm_py/Dockerfile) | Docker | 3 | 0 | 0 | 3 |
| [python/dockerFunctions/functions/spectral_norm_py/create_img.sh](/python/dockerFunctions/functions/spectral_norm_py/create_img.sh) | Shell Script | 1 | 0 | 0 | 1 |
| [python/dockerFunctions/functions/spectral_norm_py/main.py](/python/dockerFunctions/functions/spectral_norm_py/main.py) | Python | 32 | 0 | 9 | 41 |
| [python/dockerFunctions/functions/string_fetch/Dockerfile](/python/dockerFunctions/functions/string_fetch/Dockerfile) | Docker | 3 | 0 | 0 | 3 |
| [python/dockerFunctions/functions/string_fetch/create_img.sh](/python/dockerFunctions/functions/string_fetch/create_img.sh) | Shell Script | 1 | 0 | 0 | 1 |
| [python/dockerFunctions/functions/string_fetch/main.py](/python/dockerFunctions/functions/string_fetch/main.py) | Python | 20 | 0 | 7 | 27 |
| [python/dockerFunctions/functions/sum/Dockerfile](/python/dockerFunctions/functions/sum/Dockerfile) | Docker | 2 | 0 | 0 | 2 |
| [python/dockerFunctions/functions/sum/create_img.sh](/python/dockerFunctions/functions/sum/create_img.sh) | Shell Script | 1 | 0 | 0 | 1 |
| [python/dockerFunctions/functions/sum/main.py](/python/dockerFunctions/functions/sum/main.py) | Python | 3 | 0 | 2 | 5 |
| [python/dockerFunctions/functions/times2/Dockerfile](/python/dockerFunctions/functions/times2/Dockerfile) | Docker | 2 | 0 | 0 | 2 |
| [python/dockerFunctions/functions/times2/create_img.sh](/python/dockerFunctions/functions/times2/create_img.sh) | Shell Script | 1 | 0 | 0 | 1 |
| [python/dockerFunctions/functions/times2/main.py](/python/dockerFunctions/functions/times2/main.py) | Python | 3 | 0 | 2 | 5 |
| [python/dockerFunctions/functions/wordcount/Dockerfile](/python/dockerFunctions/functions/wordcount/Dockerfile) | Docker | 2 | 0 | 0 | 2 |
| [python/dockerFunctions/functions/wordcount/create_img.sh](/python/dockerFunctions/functions/wordcount/create_img.sh) | Shell Script | 1 | 0 | 0 | 1 |
| [python/dockerFunctions/functions/wordcount/main.py](/python/dockerFunctions/functions/wordcount/main.py) | Python | 7 | 0 | 2 | 9 |
| [python/function/Worker.py](/python/function/Worker.py) | Python | 162 | 21 | 29 | 212 |
| [python/function/function.py](/python/function/function.py) | Python | 132 | 36 | 30 | 198 |
| [python/function/functionInfo.py](/python/function/functionInfo.py) | Python | 34 | 0 | 3 | 37 |
| [python/function/functionManager.py](/python/function/functionManager.py) | Python | 80 | 5 | 13 | 98 |
| [python/function/portController.py](/python/function/portController.py) | Python | 25 | 0 | 4 | 29 |
| [python/function/wasmProxy.py](/python/function/wasmProxy.py) | Python | 112 | 5 | 21 | 138 |
| [python/grouping/component.py](/python/grouping/component.py) | Python | 33 | 0 | 6 | 39 |
| [python/grouping/grouping.py](/python/grouping/grouping.py) | Python | 175 | 11 | 33 | 219 |
| [python/grouping/groupingRepository.py](/python/grouping/groupingRepository.py) | Python | 35 | 0 | 8 | 43 |
| [python/grouping/workflowParser.py](/python/grouping/workflowParser.py) | Python | 75 | 0 | 7 | 82 |
| [python/setupScripts/dbSetup.py](/python/setupScripts/dbSetup.py) | Python | 49 | 1 | 12 | 62 |
| [python/setupScripts/db_setup.bash](/python/setupScripts/db_setup.bash) | Shell Script | 18 | 1 | 1 | 20 |
| [python/setupScripts/requirements.txt](/python/setupScripts/requirements.txt) | pip requirements | 8 | 0 | 0 | 8 |
| [python/storage/repoTest.py](/python/storage/repoTest.py) | Python | 7 | 0 | 5 | 12 |
| [python/storage/repository.py](/python/storage/repository.py) | Python | 72 | 0 | 18 | 90 |
| [python/test/postData.json](/python/test/postData.json) | JSON | 1 | 0 | 0 | 1 |
| [python/test/primeTest.py](/python/test/primeTest.py) | Python | 36 | 3 | 11 | 50 |
| [python/test/singleFuncTest.py](/python/test/singleFuncTest.py) | Python | 40 | 2 | 9 | 51 |
| [python/test/spectral_norm_test.py](/python/test/spectral_norm_test.py) | Python | 28 | 0 | 7 | 35 |
| [python/test/stringFetchTime.py](/python/test/stringFetchTime.py) | Python | 39 | 2 | 9 | 50 |
| [python/test/stringTest.py](/python/test/stringTest.py) | Python | 31 | 1 | 7 | 39 |
| [python/test/wasmCountTest.py](/python/test/wasmCountTest.py) | Python | 43 | 3 | 9 | 55 |
| [python/test/wasmProxytest.py](/python/test/wasmProxytest.py) | Python | 73 | 19 | 16 | 108 |
| [python/test/workflowContainerTest.py](/python/test/workflowContainerTest.py) | Python | 45 | 2 | 8 | 55 |
| [python/test/workflowTest.py](/python/test/workflowTest.py) | Python | 48 | 2 | 7 | 57 |
| [python/wasmFunctions/binarytree.wasm](/python/wasmFunctions/binarytree.wasm) | WebAssembly Text Format | 444 | 0 | 16 | 460 |
| [python/wasmFunctions/cVersion/binarytree.c](/python/wasmFunctions/cVersion/binarytree.c) | C | 41 | 0 | 14 | 55 |
| [python/wasmFunctions/cVersion/build.sh](/python/wasmFunctions/cVersion/build.sh) | Shell Script | 15 | 0 | 3 | 18 |
| [python/wasmFunctions/cVersion/cal.c](/python/wasmFunctions/cVersion/cal.c) | C | 8 | 0 | 7 | 15 |
| [python/wasmFunctions/cVersion/count.c](/python/wasmFunctions/cVersion/count.c) | C | 21 | 5 | 5 | 31 |
| [python/wasmFunctions/cVersion/cut.c](/python/wasmFunctions/cVersion/cut.c) | C | 0 | 0 | 1 | 1 |
| [python/wasmFunctions/cVersion/divide2.c](/python/wasmFunctions/cVersion/divide2.c) | C | 6 | 0 | 1 | 7 |
| [python/wasmFunctions/cVersion/prime.c](/python/wasmFunctions/cVersion/prime.c) | C | 19 | 3 | 5 | 27 |
| [python/wasmFunctions/cVersion/resize.c](/python/wasmFunctions/cVersion/resize.c) | C | 6 | 0 | 1 | 7 |
| [python/wasmFunctions/cVersion/reverse.c](/python/wasmFunctions/cVersion/reverse.c) | C | 6 | 0 | 1 | 7 |
| [python/wasmFunctions/cVersion/simple_func.c](/python/wasmFunctions/cVersion/simple_func.c) | C | 13 | 0 | 4 | 17 |
| [python/wasmFunctions/cVersion/spectral_norm.c](/python/wasmFunctions/cVersion/spectral_norm.c) | C | 28 | 1 | 9 | 38 |
| [python/wasmFunctions/cVersion/string_fetch.c](/python/wasmFunctions/cVersion/string_fetch.c) | C | 14 | 0 | 4 | 18 |
| [python/wasmFunctions/cVersion/stringupperandcount.c](/python/wasmFunctions/cVersion/stringupperandcount.c) | C | 19 | 2 | 3 | 24 |
| [python/wasmFunctions/cVersion/sum.c](/python/wasmFunctions/cVersion/sum.c) | C | 6 | 0 | 1 | 7 |
| [python/wasmFunctions/cVersion/times2.c](/python/wasmFunctions/cVersion/times2.c) | C | 6 | 0 | 1 | 7 |
| [python/wasmFunctions/cVersion/wasm_sleep.c](/python/wasmFunctions/cVersion/wasm_sleep.c) | C | 16 | 0 | 3 | 19 |
| [python/wasmFunctions/cVersion/wordcount.c](/python/wasmFunctions/cVersion/wordcount.c) | C | 22 | 0 | 5 | 27 |
| [python/wasmFunctions/cal.wasm](/python/wasmFunctions/cal.wasm) | WebAssembly Text Format | 340 | 0 | 5 | 345 |
| [python/wasmFunctions/count.wasm](/python/wasmFunctions/count.wasm) | WebAssembly Text Format | 347 | 0 | 5 | 352 |
| [python/wasmFunctions/divide2.wasm](/python/wasmFunctions/divide2.wasm) | WebAssembly Text Format | 341 | 0 | 5 | 346 |
| [python/wasmFunctions/prime.wasm](/python/wasmFunctions/prime.wasm) | WebAssembly Text Format | 344 | 0 | 5 | 349 |
| [python/wasmFunctions/resize.wasm](/python/wasmFunctions/resize.wasm) | WebAssembly Text Format | 250 | 0 | 2 | 252 |
| [python/wasmFunctions/reverse.wasm](/python/wasmFunctions/reverse.wasm) | WebAssembly Text Format | 339 | 0 | 5 | 344 |
| [python/wasmFunctions/simple_func.wasm](/python/wasmFunctions/simple_func.wasm) | WebAssembly Text Format | 302 | 0 | 5 | 307 |
| [python/wasmFunctions/spectral_norm.wasm](/python/wasmFunctions/spectral_norm.wasm) | WebAssembly Text Format | 371 | 0 | 11 | 382 |
| [python/wasmFunctions/string_fetch.wasm](/python/wasmFunctions/string_fetch.wasm) | WebAssembly Text Format | 345 | 0 | 5 | 350 |
| [python/wasmFunctions/stringupperandcount.wasm](/python/wasmFunctions/stringupperandcount.wasm) | WebAssembly Text Format | 301 | 0 | 2 | 303 |
| [python/wasmFunctions/sum.wasm](/python/wasmFunctions/sum.wasm) | WebAssembly Text Format | 342 | 0 | 4 | 346 |
| [python/wasmFunctions/times2.wasm](/python/wasmFunctions/times2.wasm) | WebAssembly Text Format | 339 | 0 | 5 | 344 |
| [python/wasmFunctions/utils/cJSON.c](/python/wasmFunctions/utils/cJSON.c) | C | 2,466 | 210 | 454 | 3,130 |
| [python/wasmFunctions/utils/cJSON.h](/python/wasmFunctions/utils/cJSON.h) | C++ | 156 | 102 | 43 | 301 |
| [python/wasmFunctions/utils/spectral_norm_util.c](/python/wasmFunctions/utils/spectral_norm_util.c) | C | 33 | 0 | 7 | 40 |
| [python/wasmFunctions/utils/spectral_norm_util.h](/python/wasmFunctions/utils/spectral_norm_util.h) | C++ | 8 | 0 | 5 | 13 |
| [python/wasmFunctions/utils/wasmUtils.c](/python/wasmFunctions/utils/wasmUtils.c) | C | 122 | 0 | 25 | 147 |
| [python/wasmFunctions/utils/wasmUtils.h](/python/wasmFunctions/utils/wasmUtils.h) | C++ | 31 | 0 | 20 | 51 |
| [python/wasmFunctions/wasm_sleep.wasm](/python/wasmFunctions/wasm_sleep.wasm) | WebAssembly Text Format | 475 | 0 | 10 | 485 |
| [python/wasmFunctions/wordcount.wasm](/python/wasmFunctions/wordcount.wasm) | WebAssembly Text Format | 1,610 | 0 | 61 | 1,671 |
| [python/workflow/gateway.py](/python/workflow/gateway.py) | Python | 119 | 5 | 15 | 139 |
| [python/workflow/mastersp.py](/python/workflow/mastersp.py) | Python | 234 | 6 | 36 | 276 |
| [python/workflow/proxy.py](/python/workflow/proxy.py) | Python | 117 | 4 | 23 | 144 |
| [python/workflow/repository.py](/python/workflow/repository.py) | Python | 70 | 1 | 15 | 86 |
| [python/workflow/workersp.py](/python/workflow/workersp.py) | Python | 217 | 7 | 35 | 259 |
| [python/yaml/singleFunction/binarytree.yaml](/python/yaml/singleFunction/binarytree.yaml) | YAML | 15 | 0 | 1 | 16 |
| [python/yaml/singleFunction/cal.yaml](/python/yaml/singleFunction/cal.yaml) | YAML | 18 | 0 | 0 | 18 |
| [python/yaml/singleFunction/count.yaml](/python/yaml/singleFunction/count.yaml) | YAML | 13 | 0 | 1 | 14 |
| [python/yaml/singleFunction/cut.yaml](/python/yaml/singleFunction/cut.yaml) | YAML | 15 | 0 | 0 | 15 |
| [python/yaml/singleFunction/divide2.yaml](/python/yaml/singleFunction/divide2.yaml) | YAML | 12 | 0 | 0 | 12 |
| [python/yaml/singleFunction/merge.yaml](/python/yaml/singleFunction/merge.yaml) | YAML | 13 | 0 | 0 | 13 |
| [python/yaml/singleFunction/prime.yaml](/python/yaml/singleFunction/prime.yaml) | YAML | 12 | 0 | 0 | 12 |
| [python/yaml/singleFunction/reverse.yaml](/python/yaml/singleFunction/reverse.yaml) | YAML | 12 | 0 | 0 | 12 |
| [python/yaml/singleFunction/simple_func.yaml](/python/yaml/singleFunction/simple_func.yaml) | YAML | 17 | 0 | 1 | 18 |
| [python/yaml/singleFunction/spectral_norm.yaml](/python/yaml/singleFunction/spectral_norm.yaml) | YAML | 15 | 0 | 1 | 16 |
| [python/yaml/singleFunction/string_fetch.yaml](/python/yaml/singleFunction/string_fetch.yaml) | YAML | 14 | 0 | 1 | 15 |
| [python/yaml/singleFunction/stringupperandcount.yaml](/python/yaml/singleFunction/stringupperandcount.yaml) | YAML | 15 | 0 | 0 | 15 |
| [python/yaml/singleFunction/sum.yaml](/python/yaml/singleFunction/sum.yaml) | YAML | 16 | 0 | 0 | 16 |
| [python/yaml/singleFunction/times2.yaml](/python/yaml/singleFunction/times2.yaml) | YAML | 12 | 0 | 0 | 12 |
| [python/yaml/singleFunction/wasm_sleep.yaml](/python/yaml/singleFunction/wasm_sleep.yaml) | YAML | 10 | 0 | 0 | 10 |
| [python/yaml/singleFunction/wordcount.yaml](/python/yaml/singleFunction/wordcount.yaml) | YAML | 15 | 0 | 0 | 15 |
| [python/yaml/workflow/wordcount.yaml](/python/yaml/workflow/wordcount.yaml) | YAML | 40 | 0 | 1 | 41 |
| [python/yaml/workflow/workflow.yaml](/python/yaml/workflow/workflow.yaml) | YAML | 90 | 0 | 1 | 91 |
| [python/yaml/yamlTest.py](/python/yaml/yamlTest.py) | Python | 10 | 0 | 4 | 14 |

[Summary](results.md) / Details / [Diff Summary](diff.md) / [Diff Details](diff-details.md)