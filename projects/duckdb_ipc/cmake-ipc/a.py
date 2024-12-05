import pyarrow as pa
from pyarrow import fs
import pandas as pd


def test_read_from_file():
    file_path = "cmake-ipc/schema-valid.arrows"

    with open(file_path, "rb") as f:
        reader = pa.ipc.open_stream(f)
        print(reader.schema)
        df = reader.read_all()
        print(df)


def get_table():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4.0, 5.0, 6.0]})
    df: pa.Table
    df = pa.Table.from_pandas(df)
    return df


def write_to_file_2(path, table):
    pa.ipc.write_table(table, path)


def write_to_file_1(path, table):
    local = fs.LocalFileSystem()
    with local.open_output_stream(path) as f:
        writer = pa.ipc.new_stream(f, table.schema)
        writer.write_table(table)


def write_to_file_3(path, table):
    BATCH_SIZE = 1
    NUM_BATCHES = 100
    with pa.OSFile(path, "wb") as sink:
        with pa.ipc.new_file(sink, table.schema) as writer:
            for row in range(NUM_BATCHES):
                batch = pa.record_batch(table.slice(row * BATCH_SIZE, BATCH_SIZE))
                writer.write_batch(batch)


def test_write_to_file_1():
    new_file = "cmake-ipc/schema-valid-new.arrows"
    df = get_table()
    write_to_file_1(new_file, df)


def _test_write_to_file_2():
    new_file = "cmake-ipc/schema-valid-new.arrows"
    df = get_table()
    write_to_file_2(new_file, df)


def _test_write_to_file_3():
    new_file = "cmake-ipc/schema-valid-new.arrows"
    df = get_table()
    write_to_file_3(new_file, df)
