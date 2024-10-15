#include <iostream>
#include <vector>
#include <memory>
#include <functional>
#include <any>

// Non-templated base class for callbacks
struct ICallback {
    // Virtual execute method that takes any type of data
    virtual void execute(const std::any& data) = 0;
    virtual ~ICallback() = default;
};

// Templated derived class that implements ICallback for a specific type T
template <typename T>
struct Callback : ICallback {
    std::function<void(T)> func; // Stored callback function

    // Constructor to initialize the callback function
    Callback(std::function<void(T)> f) : func(std::move(f)) {}

    // Override execute to cast the data to type T and invoke the callback
    void execute(const std::any& data) override {
        try {
            // Attempt to cast the data to type T
            T castedData = std::any_cast<T>(data);
            func(castedData); // Invoke the callback with the casted data
        }
        catch (const std::bad_any_cast& e) {
            // Handle the case where the cast fails
            std::cerr << "Bad any cast: " << e.what() << std::endl;
        }
    }
};

// Manager class to handle multiple callbacks
struct CallbackManager {
    // Add a new callback to the manager
    void addCallback(std::unique_ptr<ICallback> cb) {
        callbacks_.emplace_back(std::move(cb));
    }
    
    // Execute all callbacks with the provided data
    void runCallbacks(const std::any& data) const {
        for(const auto& cb : callbacks_) {
            cb->execute(data);
        }
    }
    
private:
    std::vector<std::unique_ptr<ICallback>> callbacks_; // Storage for callbacks
};

int main() {
    CallbackManager manager;
    
    // Register a callback that handles int
    manager.addCallback(std::make_unique<Callback<int>>([](int x) {
        std::cout << "Handling int: " << x << std::endl;
    }));
    
    // Register a callback that handles std::string
    manager.addCallback(std::make_unique<Callback<std::string>>([](const std::string& s) {
        std::cout << "Handling string: " << s << std::endl;
    }));
    
    // Register a callback that handles double
    manager.addCallback(std::make_unique<Callback<double>>([](double d) {
        std::cout << "Handling double: " << d << std::endl;
    }));
    
    // Execute callbacks with int data
    std::cout << "Running callbacks with int data (42):" << std::endl;
    manager.runCallbacks(42); // Only the int callback will successfully execute

    std::cout << "\nRunning callbacks with string data (\"Hello World\"):" << std::endl;
    manager.runCallbacks(std::string("Hello World")); // Only the string callback will successfully execute

    std::cout << "\nRunning callbacks with double data (3.14):" << std::endl;
    manager.runCallbacks(3.14); // Only the double callback will successfully execute

    std::cout << "\nRunning callbacks with mismatched data (bool):" << std::endl;
    manager.runCallbacks(true); // No callbacks match bool; errors will be printed

    return 0;
}