import nanoarrow as na
import pyarrow as pa

path = "cmake-ipc/schema-valid-new.arrows"
def read_stream_all(path):
    with na.ArrayStream.from_path(path) as stream:
        return stream.read_all()

x = read_stream_all(path)
print(x)
table = pa.Table(x)
print(table)

path = "cmake-ipc/schema-valid-new.arrows"
x = read_stream_all(path)
print(x)



