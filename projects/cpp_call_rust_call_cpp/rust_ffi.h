#ifndef STATE_INSPECTOR_H
#define STATE_INSPECTOR_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

// Vector inspection functions
size_t get_vector_size_wrapper(const void* state_ptr);
const char* get_vector_item_name_wrapper(const void* state_ptr, size_t index);
int get_vector_item_value_wrapper(const void* state_ptr, size_t index);

// Map inspection functions
size_t get_map_size_wrapper(const void* state_ptr);
void get_map_keys_wrapper(const void* state_ptr, const char** keys, size_t* size);
const int* get_map_values_wrapper(const void* state_ptr, const char* key, size_t* size);

// Functions exposed from Rust to C++
void rust_process_data(const void* state_ptr);
void rust_inspect_state(const void* state_ptr);

#ifdef __cplusplus
}
#endif

#endif // STATE_INSPECTOR_H

