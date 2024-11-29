use arrow_array::ffi::to_ffi;
use arrow_array::{Array, Int32Array};
use arrow_data::ffi::FFI_ArrowArray;
use arrow_schema::ffi::FFI_ArrowSchema;
use std::sync::Arc;

/// # Safety
///
/// This function is unsafe because it dereferences raw pointers.
#[no_mangle]
pub unsafe extern "C" fn create_arrow_array(
    out_array: *mut FFI_ArrowArray,
    out_schema: *mut FFI_ArrowSchema,
) {
    let array = Arc::new(Int32Array::from(vec![1, 2, 3, 4, 5])) as Arc<dyn Array>;

    let (out_array_1, out_schema_1) = to_ffi(&array.to_data()).unwrap();

    unsafe {
        *out_array = out_array_1;
        *out_schema = out_schema_1;
    }
}
