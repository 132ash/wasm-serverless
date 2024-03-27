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
#include <curl/curl.h>
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

// 回调函数，用于从libcurl接收数据
size_t WriteCallback(void *contents, size_t size, size_t nmemb, std::string *s) {
    size_t newLength = size * nmemb;
    try {
        s->append((char*)contents, newLength);
        return newLength;
    } catch (std::bad_alloc &e) {
        // 如果内存不足，返回0告诉curl停止传输
        return 0;
    }
}

std::string ExtractContentFromRawJson(std::string rawJson) {
    std::string contentKey = "\"content\":\"";
    size_t startPos = rawJson.find(contentKey);
    if (startPos == std::string::npos) {
        return ""; // "content" key not found
    }
    startPos += contentKey.length(); // Move start position to the beginning of the value
    size_t endPos = rawJson.find("\"", startPos);
    if (endPos == std::string::npos) {
        return ""; // Malformed JSON or unexpected end of content
    }
    return rawJson.substr(startPos, endPos - startPos);
}

std::string GetDocumentContent(const std::string& strKey, long long *getStringTime) {
    CURL *curl;
    CURLcode res;
    std::string readBuffer;
    long long beforeParam , afterParam;
    struct timeval tv;

    curl = curl_easy_init();
    if(curl) {
        std::string url = COUCH_URL + "/" + DATA_TRANSFER_DB + "/" + strKey;
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        res = curl_easy_perform(curl);
        curl_easy_cleanup(curl);
        if(res != CURLE_OK) {
            std::cerr << "CURL error: " << curl_easy_strerror(res) << std::endl;
        } else {
            // 解析JSON响应
            try {
                gettimeofday(&tv, NULL);
                beforeParam = (long long)tv.tv_sec * 1000000LL + (long long)tv.tv_usec;
                std::string res = ExtractContentFromRawJson(readBuffer);
                gettimeofday(&tv, NULL);
                afterParam = (long long)tv.tv_sec * 1000000LL + (long long)tv.tv_usec;
                *getStringTime = afterParam - beforeParam;
                return res;
            } catch (json::parse_error& e) {
                std::cerr << "JSON parse error: " << e.what() << std::endl;
            }
        }
    }
    return "";
}