import duckdb
import pyarrow as pa
import numpy as np
import multiprocessing
import tempfile
import os

def duckdb_high_throughput_ipc():
    def writer_process(db_path):
        # Create connection
        conn = duckdb.connect(db_path)
        
        # Create large dataset
        integers = np.arange(1_000_000, dtype=np.int64)
        floats = np.random.rand(1_000_000)
        
        # Create Arrow table
        table = pa.table({
            'integers': integers,
            'floats': floats
        })
        
        # Register table
        conn.register('large_table', table)
        
        # Persist to database
        conn.execute("CREATE TABLE data AS SELECT * FROM large_table")
        
        print("Data written to DuckDB")
        conn.close()

    def reader_process(db_path):
        # Create connection
        conn = duckdb.connect(db_path)
        
        # Read data
        result = conn.execute("SELECT * FROM data LIMIT 10").fetchdf()
        
        print(f"Read {len(result)} rows")
        print("First few rows:")
        print(result)
        
        # Get total row count
        row_count = conn.execute("SELECT COUNT(*) FROM data").fetchone()[0]
        print(f"Total rows: {row_count}")
        
        conn.close()

    # Create temporary database file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as temp_db:
        db_path = temp_db.name

    # Create processes
    writer = multiprocessing.Process(
        target=writer_process, 
        args=(db_path,)
    )
    reader = multiprocessing.Process(
        target=reader_process, 
        args=(db_path,)
    )
    
    writer.start()
    reader.start()
    
    writer.join()
    reader.join()
    
    # Cleanup
    os.unlink(db_path)

if __name__ == '__main__':
    duckdb_high_throughput_ipc()