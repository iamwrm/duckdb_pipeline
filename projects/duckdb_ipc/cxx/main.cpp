#include <arrow/array.h>
#include <arrow/builder.h>
#include <arrow/c/bridge.h>
#include <iostream>

// Import the Rust function
extern "C" {
void create_arrow_array(struct ArrowArray *out_array,
                        struct ArrowSchema *out_schema);
}

int main(int argc, char **argv) {
  // Allocate FFI structures
  struct ArrowArray array;
  struct ArrowSchema schema;

  bool use_cpp = argc > 1 && std::string(argv[1]) == "cpp";

  if (use_cpp) {

    // Create a simple array
    arrow::Int32Builder builder;
    auto status1 = builder.Append(1);
    if (!status1.ok()) {
      std::cerr << "Error appending value 1: " << status1.ToString()
                << std::endl;
      return 1;
    }
    auto status2 = builder.Append(2);
    if (!status2.ok()) {
      std::cerr << "Error appending value 2: " << status2.ToString()
                << std::endl;
      return 1;
    }
    auto status3 = builder.Append(3);
    if (!status3.ok()) {
      std::cerr << "Error appending value 3: " << status3.ToString()
                << std::endl;
      return 1;
    }

    // Get the array from the builder
    std::shared_ptr<arrow::Array> built_array;
    auto status = builder.Finish(&built_array);
    if (!status.ok()) {
      std::cerr << "Error building array: " << status.ToString() << std::endl;
      return 1;
    }

    // Export the array to C Data Interface
    status = arrow::ExportArray(*built_array, &array, &schema);
    if (!status.ok()) {
      std::cerr << "Error exporting array: " << status.ToString() << std::endl;
      return 1;
    }
  } else {
    create_arrow_array(&array, &schema);
  }

  // Now import it back
  std::shared_ptr<arrow::Array> arrow_array;
  arrow::Result<std::shared_ptr<arrow::Array>> result =
      arrow::ImportArray(&array, &schema);

  if (result.ok()) {
    arrow_array = result.ValueOrDie();

    // Use the array
    auto int32_array = std::static_pointer_cast<arrow::Int32Array>(arrow_array);
    for (int i = 0; i < int32_array->length(); i++) {
      std::cout << int32_array->Value(i) << " ";
    }
  }

  return 0;
}