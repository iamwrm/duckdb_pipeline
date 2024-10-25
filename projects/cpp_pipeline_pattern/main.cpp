#include <functional>
#include <string>
#include <vector>
#include <cstdio>

#include <optional>

struct Person {
    std::optional<std::string> name;
    std::optional<int> age;
};


class Pipeline {
private:
    using Handler = std::function<std::string(std::string, std::function<std::string(std::string)>)>;
    std::vector<Handler> handlers;

public:
    void use(Handler middleware) {
        handlers.push_back(middleware);
    }
    
    std::string process(std::string input) {
        if (handlers.empty()) {
            return input;
        }
        
        size_t index = 0;
        
        std::function<std::string(std::string)> next = [&](std::string str) {
            if (index >= handlers.size()) {
                return str;
            }
            printf("index: %zu\n", index);
            return handlers[index++](str, next);
        };
        
        return next(input);
    }
};

// Example usage:
int main() {
    Pipeline pipeline;
    
    // Add middleware functions
    pipeline.use([](std::string data, auto next) {
        data += " -> First";
        printf("First: %s\n", data.c_str());
        return next(data);
    });
    
    pipeline.use([](std::string data, auto next) {
        data += " -> Second";
        printf("Second: %s\n", data.c_str());
        return next(data);
    });
    
    pipeline.use([](std::string data, auto next) {
        data += " -> Third";
        printf("Third: %s\n", data.c_str());
        return data; // End of pipeline
    });
    
    std::string result = pipeline.process("Start");
    printf("%s\n", result.c_str());
    // Result: "Start -> First -> Second -> Third"

    // Usage example:
    Person p1{.name="John", .age=std::nullopt};
    // Person p2{.name="Bob", .age=std::nullopt, .parent=p1};
    // Person p3{.name="Alice", .age=std::nullopt, .parent=p2};
    
    return 0;
}