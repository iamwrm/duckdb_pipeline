import nanoarrow as na

path = "cmake-ipc/schema-valid.arrows"
def read_stream_all(path):
    with na.ArrayStream.from_path(path) as stream:
        return stream.read_all()

x = read_stream_all(path)
print(x)

path = "cmake-ipc/schema-valid-new.arrows"
x = read_stream_all(path)
print(x)



