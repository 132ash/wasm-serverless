#include <nlohmann/json.hpp>

using json = nlohmann::json;

json mainFunction(const json& reqBody) {
    int sum = 0;
    for (const auto& item : reqBody) {
        sum += item.get<int>(); // 假设所有提供的都是整数
    }
    return json{{"sum", sum}};
}