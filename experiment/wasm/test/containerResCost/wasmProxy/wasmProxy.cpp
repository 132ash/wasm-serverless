#include <unistd.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <cstring>
#include <vector>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <array>
#include "httplib.h"
#include "json.hpp"
#define PIPE_WRITE_FD 10713
#define STATE_WRITE_FD 10714

using json = nlohmann::json;
// std::string workerPath =  "/home/ash/wasm/wasm-serverless/cppWasmWorker/worker_INTERP/build/worker";
std::string workerPath =  "/home/ash/wasm/wasm-serverless/cppWasmWorker/worker_JIT/build/worker";

class Runner {
public:
    std::string wasmCodePath;
    std::string funcName;
    size_t outputSize;
    size_t heapSize;
    int in_fd;
    int out_fd;
    int state_fd;
    pid_t workerPid;
    const std::string message = "ready\n";

    Runner() : outputSize(0), in_fd(0), out_fd(1), state_fd(2), workerPid(0) {}

    void init(const std::string &wasmPath, const std::string &func, size_t outputSz, size_t heapSz) {
        std::cout << "init" << std::endl;
        wasmCodePath = wasmPath;
        funcName = func;
        outputSize = outputSz;
        heapSize = heapSz;

        int p1[2], p2[2], p3[2];
        pipe(p1);
        pipe(p2);
        pipe(p3);

        workerPid = fork();
        if (workerPid > 0) {  // Parent process
            in_fd = p1[1];
            out_fd = p2[0];
            state_fd = p3[0];
            close(p1[0]);
            close(p2[1]);
            close(p3[1]);
            write(in_fd, (wasmCodePath + "\n").c_str(), wasmCodePath.length() + 1);
            write(in_fd, (funcName + "\n").c_str(), funcName.length() + 1);
            std::string outSizeStr = std::to_string(outputSize) + "\n";
            std::string heapSizeStr = std::to_string(heapSize) + "\n";
            write(in_fd, outSizeStr.c_str(), outSizeStr.length());
            write(in_fd, heapSizeStr.c_str(), heapSizeStr.length());
            
        } else {  // Child process
            dup2(p1[0], STDIN_FILENO);
            dup2(p2[1], PIPE_WRITE_FD);
            dup2(p3[1], STATE_WRITE_FD);
            close(p1[1]);
            close(p2[0]);
            close(p3[0]);

            execl(workerPath.c_str(), "worker", nullptr);
            std::cerr << "Execution failed!" << std::endl;
            exit(1);
        }
    }

    std::string getState() {
        char buffer[128];
        read(state_fd, buffer, message.length());
        return std::string(buffer);
    }

    std::string getResultFromPipe() {
        std::string result;
        char buffer[4096];
        while (result.size() < outputSize + 16) {
            ssize_t count = read(out_fd, buffer, sizeof(buffer));
            if (count == 0) break;  // Pipe closed
            result.append(buffer, count);
        }
        return result;
    }

    std::string run(const std::string &param) {
        std::string msg = getState();
        if (msg == message) {
            write(in_fd, param.c_str(), param.length());
            std::string res = getResultFromPipe();
            return base64_encode(res);
        }
        std::cout << "get null" << std::endl;
        return base64_encode("");
    }

    inline std::string base64_encode(const std::string &in) {
    static const auto lookup =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

    std::string out;
    out.reserve(in.size());

    int val = 0;
    int valb = -6;

    for (auto c : in) {
        val = (val << 8) + static_cast<uint8_t>(c);
        valb += 8;
        while (valb >= 0) {
        out.push_back(lookup[(val >> valb) & 0x3F]);
        valb -= 6;
        }
    }

    if (valb > -6) { out.push_back(lookup[((val << 8) >> (valb + 8)) & 0x3F]); }

    while (out.size() % 4) {
        out.push_back('=');
    }

    return out;
    }
};


Runner runner;


int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " <port>" << std::endl;
        return 1;
    }

    int port = std::stoi(argv[1]);
    httplib::Server svr;


    svr.Get("/status", [&](const httplib::Request&, httplib::Response& res) {
        try {
            json response = {{"status", "running"}};
            if (!runner.funcName.empty()) {
                response["function"] = runner.funcName;
            }
            res.set_content(response.dump(), "application/json");
            res.status = 200;
        } catch (const std::exception& e) {
            std::cerr << "Exception in /status endpoint: " << e.what() << std::endl;
        }
    });

    svr.Post("/init", [&](const httplib::Request& req, httplib::Response& res) {

        
        auto inp = json::parse(req.body);
        try {
            runner.init(inp["wasmCodePath"], inp["funcName"], inp["outputSize"], 65536);
        } catch (const std::exception& e) {
            std::cerr << "Error initializing runner: " << e.what() << std::endl;
            // Handle error, e.g., set HTTP response to indicate failure
        }
        json response = {
            {"status", "initialized"}
        };
        res.set_content(response.dump(), "application/json");
        res.status = 200;
    });

    svr.Post("/run", [&](const httplib::Request& req, httplib::Response& res) {
        auto inp = json::parse(req.body);
        std::string output = runner.run(inp["parameters"]);
        json response = {
            {"out", output}
        };
        std::cout << output << std::endl;
        res.set_content(response.dump(), "application/json");
        res.status = 200;
    });

    std::cout << "Server started on port " << port << std::endl;
    svr.listen("localhost", port);
}