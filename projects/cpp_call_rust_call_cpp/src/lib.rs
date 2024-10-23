// lib.rs
use std::ffi::{c_void, CStr, c_char};
use std::slice;

#[repr(C)]
pub struct StateInspector {
    state_ptr: *const c_void,
}

extern "C" {
    fn get_vector_size_wrapper(state_ptr: *const c_void) -> usize;
    fn get_vector_item_name_wrapper(state_ptr: *const c_void, index: usize) -> *const c_char;
    fn get_vector_item_value_wrapper(state_ptr: *const c_void, index: usize) -> i32;
    fn get_map_size_wrapper(state_ptr: *const c_void) -> usize;
    fn get_map_keys_wrapper(state_ptr: *const c_void, keys: *mut *const c_char, size: *mut usize);
    fn get_map_values_wrapper(state_ptr: *const c_void, key: *const c_char, size: *mut usize) -> *const i32;
}

impl StateInspector {
    fn new(ptr: *const c_void) -> Self {
        StateInspector { state_ptr: ptr }
    }

    fn inspect_vector(&self) {
        unsafe {
            let vec_size = get_vector_size_wrapper(self.state_ptr);
            println!("Rust: Vector contains {} items:", vec_size);
            
            for i in 0..vec_size {
                let name_ptr = get_vector_item_name_wrapper(self.state_ptr, i);
                let name = CStr::from_ptr(name_ptr).to_string_lossy();
                let value = get_vector_item_value_wrapper(self.state_ptr, i);
                println!("  {}: {}", name, value);
            }
        }
    }

    fn inspect_map(&self) {
        unsafe {
            let map_size = get_map_size_wrapper(self.state_ptr);
            let mut keys: Vec<*const c_char> = vec![std::ptr::null(); map_size];
            let mut actual_size = map_size;
            
            get_map_keys_wrapper(self.state_ptr, keys.as_mut_ptr(), &mut actual_size);
            
            println!("Rust: Map contains {} entries:", actual_size);
            
            for i in 0..actual_size {
                let key = CStr::from_ptr(keys[i]).to_string_lossy();
                let mut values_size: usize = 0;
                let values_ptr = get_map_values_wrapper(
                    self.state_ptr,
                    keys[i],
                    &mut values_size
                );
                
                if !values_ptr.is_null() {
                    let values = slice::from_raw_parts(values_ptr, values_size);
                    print!("  {}: ", key);
                    for value in values {
                        print!("{} ", value);
                    }
                    println!();
                }
            }
        }
    }
}

#[no_mangle]
pub extern "C" fn rust_process_data(state_ptr: *const c_void) {
    println!("Rust: Processing data from C++ state");
    let inspector = StateInspector::new(state_ptr);
    inspector.inspect_vector();
    inspector.inspect_map();
}

#[no_mangle]
pub extern "C" fn rust_inspect_state(state_ptr: *const c_void) {
    println!("\nRust: Inspecting full state");
    let inspector = StateInspector::new(state_ptr);
    inspector.inspect_vector();
    inspector.inspect_map();
}