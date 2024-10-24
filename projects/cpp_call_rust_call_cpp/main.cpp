// main.cpp
#include <cstdint>
#include <iostream>
#include <map>
#include <string>
#include <vector>
#include "rust_ffi.h"

struct StateData {
  std::string name;
  int value;

  StateData(std::string n, int v) : name(n), value(v) {}
};

extern "C" {
void rust_inspect_state(const void *state_ptr);
void rust_process_data(const void *state_ptr);
}

class ComplexStateManager {
private:
  std::vector<StateData> data_vector;
  std::map<std::string, std::vector<int>> data_map;
  uint64_t counter;

public:
  ComplexStateManager() : counter(0) {}

  // Getter functions exposed to Rust
  static size_t get_vector_size(const ComplexStateManager *self) {
    return self->data_vector.size();
  }

  static const char *get_vector_item_name(const ComplexStateManager *self,
                                          size_t index) {
    if (index < self->data_vector.size()) {
      return self->data_vector[index].name.c_str();
    }
    return "";
  }

  static int get_vector_item_value(const ComplexStateManager *self,
                                   size_t index) {
    if (index < self->data_vector.size()) {
      return self->data_vector[index].value;
    }
    return -1;
  }

  static size_t get_map_size(const ComplexStateManager *self) {
    return self->data_map.size();
  }

  static void get_map_keys(const ComplexStateManager *self, const char **keys,
                           size_t *size) {
    size_t i = 0;
    for (const auto &pair : self->data_map) {
      if (i < *size) {
        keys[i] = pair.first.c_str();
        i++;
      }
    }
    *size = i;
  }

  static const int *get_map_values(const ComplexStateManager *self,
                                   const char *key, size_t *size) {
    auto it = self->data_map.find(key);
    if (it != self->data_map.end()) {
      *size = it->second.size();
      return it->second.data();
    }
    *size = 0;
    return nullptr;
  }

  void update_state() {
    counter++;

    // Update vector
    data_vector.emplace_back("item_" + std::to_string(counter), counter * 10);

    // Update map
    std::string key = "group_" + std::to_string(counter % 3);
    data_map[key].push_back(counter);

    std::cout << "C++: State updated:\n";
    print_state();
  }

  void process() {
    std::cout << "C++: Processing data, calling Rust...\n";
    rust_process_data(this);
    rust_inspect_state(this);
  }

  void print_state() const {
    std::cout << "Vector contents:\n";
    for (const auto &item : data_vector) {
      std::cout << "  " << item.name << ": " << item.value << "\n";
    }

    std::cout << "Map contents:\n";
    for (const auto &[key, values] : data_map) {
      std::cout << "  " << key << ": ";
      for (int value : values) {
        std::cout << value << " ";
      }
      std::cout << "\n";
    }
  }
};

// Export C-style functions for Rust to call
extern "C" {
size_t get_vector_size_wrapper(const void *state_ptr) {
  return ComplexStateManager::get_vector_size(
      static_cast<const ComplexStateManager *>(state_ptr));
}

const char *get_vector_item_name_wrapper(const void *state_ptr, size_t index) {
  return ComplexStateManager::get_vector_item_name(
      static_cast<const ComplexStateManager *>(state_ptr), index);
}

int get_vector_item_value_wrapper(const void *state_ptr, size_t index) {
  return ComplexStateManager::get_vector_item_value(
      static_cast<const ComplexStateManager *>(state_ptr), index);
}

size_t get_map_size_wrapper(const void *state_ptr) {
  return ComplexStateManager::get_map_size(
      static_cast<const ComplexStateManager *>(state_ptr));
}

void get_map_keys_wrapper(const void *state_ptr, const char **keys,
                          size_t *size) {
  ComplexStateManager::get_map_keys(
      static_cast<const ComplexStateManager *>(state_ptr), keys, size);
}

const int *get_map_values_wrapper(const void *state_ptr, const char *key,
                                  size_t *size) {
  return ComplexStateManager::get_map_values(
      static_cast<const ComplexStateManager *>(state_ptr), key, size);
}
}

int main() {
  ComplexStateManager state;

  // Update state multiple times
  for (int i = 0; i < 5; i++) {
    state.update_state();
    state.process();
  }

  return 0;
}