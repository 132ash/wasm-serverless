#include "httplib.h"
#include <nlohmann/json.hpp>
#include <chrono>

// 使用nlohmann/json库
using json = nlohmann::json;

std::string status = "new";
std::string functionName = "None";

// 声明mainFunction，它现在接收一个json对象作为参数
json mainFunction(const json& reqBody);

int main() {
    using namespace httplib;
    Server svr;

    // return status and workdir of container.
    svr.Get("/status", [](const httplib::Request& req, httplib::Response& res){
        json data;
        data["status"] = status;
        data["function"] = functionName;
        res.set_content(data.dump(), "application/json");
    });


    // init: just set status to ok. 
    svr.Post("/init", [](const Request& req, Response& res) {
        status = "ok";
        auto decodedJson = json::parse(req.body);
        functionName = decodedJson["function"].get<std::string>();
        json response;
        response["message"] = "Init successfully.";
        res.set_content(response.dump(), "application/json");
    });


    svr.Post("/run", [](const Request& req, Response& res) {
        try {
            // 解析请求体为JSON对象
            auto reqBody = json::parse(req.body);

            // 获取当前时间戳
            auto start = std::chrono::high_resolution_clock::now();
            auto start_time = std::chrono::time_point_cast<std::chrono::microseconds>(start).time_since_epoch().count();

            // 调用mainFunction
            auto result = mainFunction(reqBody);

            // 构建响应JSON
            json response;
            response["out"] = result;
            response["startTime"] = start_time;

            res.set_content(response.dump(), "application/json");
        } catch (std::exception& e) {
            res.status = 400;
            json errorResponse;
            errorResponse["error"] = e.what();
            res.set_content(errorResponse.dump(), "application/json");
        }
    });

    svr.listen("0.0.0.0", 5000);
}
