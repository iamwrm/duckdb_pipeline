use arrow::array::{Array, StringArray, Int32Array};
use arrow::datatypes::{DataType, Field, Schema};
use arrow::ipc::writer::FileWriter;
use arrow::record_batch::RecordBatch;
use serde::{Deserialize, Serialize};
use std::io::Cursor;
use std::sync::Arc;

#[derive(Debug, Serialize, Deserialize)]
struct Person {
    name: String,
    age: i32,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Create sample data
    let person = Person {
        name: "Alice".to_string(),
        age: 30,
    };

    let buf = {
        // Define Arrow schema
        let schema = Schema::new(vec![
            Field::new("name", DataType::Utf8, false),
            Field::new("age", DataType::Int32, false),
        ]);
        // Convert to Arrow arrays
        let name_array = StringArray::from(vec![person.name.as_str()]);
        let age_array = arrow::array::Int32Array::from(vec![person.age]);
        // Create record batch
        let batch = RecordBatch::try_new(
            Arc::new(schema.clone()),
            vec![
                Arc::new(name_array) as Arc<dyn Array>,
                Arc::new(age_array) as Arc<dyn Array>,
            ],
        )?;
        // Write to bytes using Arrow IPC format
        let mut buf = Vec::new();
        {
            let cursor = Cursor::new(&mut buf);
            let mut writer = FileWriter::try_new(cursor, &schema)?;
            writer.write(&batch)?;
            writer.finish()?;
        }

        // Reading back from bytes (verification)
        let cursor = Cursor::new(&buf);
        let reader = arrow::ipc::reader::FileReader::try_new(cursor, None)?;

        for maybe_batch in reader {
            let batch = maybe_batch?;
            println!("Read batch: {:?}", batch);
        }
        buf
    };

    println!("Arrow IPC bytes length: {}", buf.len());
    println!("First few bytes: {:?}", &buf[..20]);

    // Bytes to struc
    let cursor = Cursor::new(&buf);
    let reader = arrow::ipc::reader::FileReader::try_new(cursor, None)?;
    let batch = reader.into_iter().next().unwrap()?;

    // Extract values from the batch
    let name_array = batch
        .column(0)
        .as_any()
        .downcast_ref::<StringArray>()
        .unwrap();
    let age_array = batch
        .column(1)
        .as_any()
        .downcast_ref::<Int32Array>()
        .unwrap();

    // Create Person struct from Arrow arrays
    let reconstructed_person = Person {
        name: name_array.value(0).to_string(),
        age: age_array.value(0),
    };

    println!("Reconstructed person: {:?}", reconstructed_person);

    Ok(())
}
