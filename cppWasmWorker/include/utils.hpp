#include <cstdint>
#include <vector>
#include <string>
#include <cstring>
#include <stdexcept>
#include <iostream>
#include <unistd.h>
#include <fcntl.h>
#include <sstream>
#include <time.h>
#include <cpr/cpr.h>
#include <wasm_exec_env.h>
#include <wasm_export.h>
#include "../include/json.hpp"

using json = nlohmann::json;

std::string COUCH_URL = "http://132ash:ash020620@192.168.35.132:5984";
std::string DATA_TRANSFER_DB = "strings_for_data_transfer";


bool compare_pred(unsigned char a, unsigned char b) {
	return std::tolower(a) == std::tolower(b);
}
bool EndsWith(const std::string& str, const std::string& suffix) {
 
	if (str.size() < suffix.size()) {
		return false;
	}
 
	std::string tstr = str.substr(str.size() - suffix.size());
 
	if (tstr.length() == suffix.length()) {
		return std::equal(suffix.begin(), suffix.end(), tstr.begin(), compare_pred);
	} else {
		return false;
	}
}


void readBytes(int fd, unsigned char* buffer, int bufferLength){
    int cpos = 0;
    while (cpos < bufferLength) {
        int rc = read(fd, buffer + cpos, bufferLength - cpos);
        if (rc < 0) {
            perror("[Host Worker Read] Couldn't Read from worker.");
            throw "[Host Worker Read] Couldn't Read from worker.";
        } else {
            cpos += rc;
        }
    }
}


void readFileToBytes(const std::string& path, std::vector<uint8_t>& codeBytes){
    int fd = open(path.c_str(), O_RDONLY);
    if (fd < 0) throw std::runtime_error("Couldn't open file " + path);
    struct stat statbuf;
    int staterr = fstat(fd, &statbuf);
    if (staterr < 0) throw std::runtime_error("Couldn't stat file " + path);
    size_t fsize = statbuf.st_size;
    posix_fadvise(fd, 0, 0, POSIX_FADV_SEQUENTIAL);
    codeBytes.resize(fsize);
    readBytes(fd, codeBytes.data(), fsize);
    close(fd);
    return;
}

// // 回调函数，用于从libcurl接收数据
// size_t WriteCallback(void *contents, size_t size, size_t nmemb, std::string *s) {
//     size_t newLength = size * nmemb;
//     try {
//         s->append((char*)contents, newLength);
//         return newLength;
//     } catch (std::bad_alloc &e) {
//         // 如果内存不足，返回0告诉curl停止传输
//         return 0;
//     }
// }

// std::string ExtractContentFromRawJson(std::string rawJson) {
//     std::string contentKey = "\"content\":\"";
//     size_t startPos = rawJson.find(contentKey);
//     if (startPos == std::string::npos) {
//         return ""; // "content" key not found
//     }
//     startPos += contentKey.length(); // Move start position to the beginning of the value
//     size_t endPos = rawJson.find("\"", startPos);
//     if (endPos == std::string::npos) {
//         return ""; // Malformed JSON or unexpected end of content
//     }
//     return rawJson.substr(startPos, endPos - startPos);
// }

std::string GetDocumentContent(const std::string& strKey, long long *getStringTime) {
    std::string url = COUCH_URL + "/" + DATA_TRANSFER_DB + "/" + strKey;
    *getStringTime = 0;
    struct timeval tv;

    gettimeofday(&tv, NULL);
    *getStringTime = (long long)tv.tv_sec * 1000000LL + (long long)tv.tv_usec;
    auto response = cpr::Get(cpr::Url{url});
    gettimeofday(&tv, NULL);
    *getStringTime = (long long)tv.tv_sec * 1000000LL + (long long)tv.tv_usec - *getStringTime;

    if (response.status_code == 200) { // HTTP OK
        // 直接查找content值，避免解析整个JSON
        std::string contentKey = "\"content\":\"";
        size_t startPos = response.text.find(contentKey);
        if (startPos != std::string::npos) {
            startPos += contentKey.length();
            size_t endPos = response.text.find("\"", startPos);
            if (endPos != std::string::npos) {
                return response.text.substr(startPos, endPos - startPos);
            }
        }
    }
    // } else {
    //     std::cerr << "Failed to get document. Status code: " << response.status_code << std::endl;
    // }

    return "nullstring"; // 返回空字符串表示未找到或出错
}