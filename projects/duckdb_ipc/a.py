import pyarrow as pa
import pyarrow.ipc as ipc
import multiprocessing
import os
import tempfile

def writer_process(file_path):
    # Create an Arrow table
    arrays = [
        pa.array([1, 2, 3, 4, 5]),
        pa.array(['a', 'b', 'c', 'd', 'e'])
    ]
    table = pa.table(arrays, names=['numbers', 'letters'])
    
    # Write to Arrow IPC file
    with open(file_path, 'wb') as f:
        writer = ipc.new_file(f, table.schema)
        writer.write_table(table)
        writer.close()
    
    print("Writer: Wrote table to IPC file")

def reader_process(file_path):
    # Read from Arrow IPC file
    with open(file_path, 'rb') as f:
        reader = ipc.open_file(f)
        reconstructed_table = reader.read_all()
        
    # Print the reconstructed table
    print("Reader: Reconstructed Table:")
    print(reconstructed_table)
    print("\nReader: Table Details:")
    print(f"Number of rows: {reconstructed_table.num_rows}")
    print(f"Number of columns: {reconstructed_table.num_columns}")

def main():
    # Create a temporary file for IPC
    with tempfile.NamedTemporaryFile(delete=False, suffix='.arrow') as temp_file:
        file_path = temp_file.name
    
    # Create processes
    writer = multiprocessing.Process(
        target=writer_process, 
        args=(file_path,)
    )
    reader = multiprocessing.Process(
        target=reader_process, 
        args=(file_path,)
    )
    
    # Start processes
    writer.start()
    writer.join()  # Wait for writer to finish
    
    reader.start()
    reader.join()  # Wait for reader to finish
    
    # Clean up temporary file
    os.unlink(file_path)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()