#include <stdio.h>
#include <curl/curl.h>

size_t write_data(void *ptr, size_t size, size_t nmemb, void *stream) {
    return fwrite(ptr, size, nmemb, stdout);
}

int main(void) {
    CURL *curl;
    CURLcode res;
    char *url = "https://www.google.com";
    
    curl = curl_easy_init();
    if (curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_data);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, NULL);
        res = curl_easy_perform(curl);
        curl_easy_cleanup(curl);
    }
    return 0;
}