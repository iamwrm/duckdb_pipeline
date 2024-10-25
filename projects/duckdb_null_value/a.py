import duckdb

duckdb.sql("""
CREATE TABLE a(i STRUCT(a INTEGER, b INTEGER, c STRUCT(d INTEGER, e INTEGER)));
""")

duckdb.sql("""
    INSERT INTO a VALUES 
    ({a : 1, b : 2, c : {d : 3, e : 4}}), 
    ({a : 5, b : 6, c : {d : 7, e : 8}}), 
    ({a : 9, b : 10, c : {d : 11, e : 12}})
""")


duckdb.sql("SELECT * FROM a").show()

print(duckdb.sql("SELECT i FROM a").fetchall())

duckdb.sql("SELECT i.* FROM a").show()

duckdb.sql("""
    SELECT 
        xx.*,
        i.*
    FROM (
        SELECT 
            i.c as xx,
            i
        FROM a
    ) xx
""").show()

duckdb.sql("""
    SELECT 
        i.*
    FROM a
""").show()
