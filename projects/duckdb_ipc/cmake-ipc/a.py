import pyarrow as pa
from pyarrow import fs
import pandas as pd


print(pa.__file__)

file_path = "cmake-ipc/schema-valid.arrows"

with open(file_path, "rb") as f:
    reader = pa.ipc.open_stream(f)
    print(reader.schema)
    df = reader.read_all()
    print(df)

new_file = "cmake-ipc/schema-valid-new.arrows"
df = pd.DataFrame({"a": [1, 2, 3], "b": [4.0, 5.0, 6.0]})

df: pa.Table
df = pa.Table.from_pandas(df)
print(df)

local = fs.LocalFileSystem()
with local.open_output_stream(new_file) as f:
    writer = pa.ipc.new_stream(f, df.schema)
    writer.write_table(df)
