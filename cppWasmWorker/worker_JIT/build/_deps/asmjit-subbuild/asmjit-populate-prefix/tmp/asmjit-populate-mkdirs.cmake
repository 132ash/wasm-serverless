# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "/home/ash/wasm/wasm-serverless/cppWasmWorker/worker_JIT/build/_deps/asmjit-src"
  "/home/ash/wasm/wasm-serverless/cppWasmWorker/worker_JIT/build/_deps/asmjit-build"
  "/home/ash/wasm/wasm-serverless/cppWasmWorker/worker_JIT/build/_deps/asmjit-subbuild/asmjit-populate-prefix"
  "/home/ash/wasm/wasm-serverless/cppWasmWorker/worker_JIT/build/_deps/asmjit-subbuild/asmjit-populate-prefix/tmp"
  "/home/ash/wasm/wasm-serverless/cppWasmWorker/worker_JIT/build/_deps/asmjit-subbuild/asmjit-populate-prefix/src/asmjit-populate-stamp"
  "/home/ash/wasm/wasm-serverless/cppWasmWorker/worker_JIT/build/_deps/asmjit-subbuild/asmjit-populate-prefix/src"
  "/home/ash/wasm/wasm-serverless/cppWasmWorker/worker_JIT/build/_deps/asmjit-subbuild/asmjit-populate-prefix/src/asmjit-populate-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/home/ash/wasm/wasm-serverless/cppWasmWorker/worker_JIT/build/_deps/asmjit-subbuild/asmjit-populate-prefix/src/asmjit-populate-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "/home/ash/wasm/wasm-serverless/cppWasmWorker/worker_JIT/build/_deps/asmjit-subbuild/asmjit-populate-prefix/src/asmjit-populate-stamp${cfgdir}") # cfgdir has leading slash
endif()
