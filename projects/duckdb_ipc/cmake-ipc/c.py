import pandas as pd
import pyarrow as pa
from nanoarrow.c_array import allocate_c_array

array = allocate_c_array()
pa.array([1, 2, 3])._export_to_c(array._addr())

table = pa.Table.from_pandas(
    pd.DataFrame({"numbers": [1, 2, 3], "letters": ["a", "b", "c"]})
)

na_array = allocate_c_array()
a = table.columns[0].combine_chunks()
print(a)
a._export_to_c(na_array._addr())
print(na_array)

na_array = allocate_c_array()
b = table.columns[1].combine_chunks()
print(b)
b._export_to_c(na_array._addr())
print(na_array)