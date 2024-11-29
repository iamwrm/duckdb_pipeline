import pyarrow as pa
import multiprocessing
import os
import tempfile
import pickle

def writer_process(file_path):
    # Create an Arrow table
    arrays = [
        pa.array([1, 2, 3, 4, 5]),
        pa.array(['a', 'b', 'c', 'd', 'e'])
    ]
    table = pa.table(arrays, names=['numbers', 'letters'])
    
    # Serialize the table using pickle
    with open(file_path, 'wb') as f:
        pickle.dump(table, f)
    
    print("Writer: Wrote table to file")

def reader_process(file_path):
    # Deserialize the table
    with open(file_path, 'rb') as f:
        reconstructed_table = pickle.load(f)
        
    # Print the reconstructed table
    print("Reader: Reconstructed Table:")
    print(reconstructed_table)
    print("\nReader: Table Details:")
    print(f"Number of rows: {reconstructed_table.num_rows}")
    print(f"Number of columns: {reconstructed_table.num_columns}")

def main():
    # Create a temporary file for IPC
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
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