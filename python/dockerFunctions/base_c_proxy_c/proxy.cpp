#include "include/httplib.h"
#include "include/json.hpp"
#include <string>
#include <vector>
#include <chrono>
#include <cstdlib>
#include <cstdio>
#include <iostream>
#include <exception>
#include <boost/process.hpp>
#include <boost/filesystem.hpp>

using json = nlohmann::json;
namespace bp = boost::process;

std::string work_dir = "/proxy";
std::string default_file = "./main";

class Runner {
public:
    std::string function;
    std::string filePath="/proxy/main";
    json ctx;

    void init(const std::string& func) {
        std::cout << "init..." << std::endl;
        function = func;
        std::cout << "init finished..." << std::endl;
    }

    json run(const json& params) {
        std::cout << "run." << std::endl;
        ctx = params;
        std::vector<std::string> param_list;
        std::string param;
        for (auto& item : params.items()) {
            try  
                {  
                   param = std::to_string(item.value().get<int>());
                }  
                catch (std::exception& e)  
                {  
                    std::cout << "Standard exception: " << e.what() << std::endl;  
                }  
            std::cout << param << std::endl;
            param_list.push_back(param);
        }
        std::string output;
        auto start = std::chrono::high_resolution_clock::now();

        bp::ipstream is;
        std::cout << "in child." << std::endl;
        bp::child c(filePath, bp::args(param_list), bp::std_out > is);
        c.wait();

        std::string line;
        while (std::getline(is, line)) {
            output += line + "\n";
        }
        std::cout << output << std::endl;

        auto end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> elapsed = end - start;

        json result = {
            {"result", output},
            {"time", elapsed.count()}
        };
        return result;
    }
};

int main() {
    httplib::Server svr;
    Runner runner;

    svr.Get("/status", [&runner](const httplib::Request&, httplib::Response& res) {
        json response = {
            {"status", "new"},
        };
        if (!runner.function.empty()) {
            response["function"] = runner.function;
        }
        res.set_content(response.dump(), "application/json");
    });

    svr.Post("/init", [&runner](const httplib::Request& req, httplib::Response& res) {
        auto inp = json::parse(req.body);
        runner.init(inp["function"].get<std::string>());
        res.set_content("OK", "text/plain");
    });

    svr.Post("/run", [&runner](const httplib::Request& req, httplib::Response& res) {
        auto inp = json::parse(req.body);
        json out = runner.run(inp);
        res.set_content(out.dump(), "application/json");
    });

    svr.listen("0.0.0.0", 5000);
}