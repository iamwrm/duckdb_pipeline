import duckdb

conn = duckdb.connect()
conn.sql("CREATE TABLE test (id INTEGER, name STRING)")
conn.sql("INSERT INTO test VALUES (1, 'Alice'), (2, 'Bob'), (3, 'Charlie')")
conn.sql("SELECT * FROM test").show()
conn.sql("COPY (SELECT * FROM test) TO 'test.csv' WITH (FORMAT 'csv')")

conn.close()

