#include <duckdb.h>
#include <fmt/core.h>

#include <catch2/catch_test_macros.hpp>
#include <cstdio>

template <typename... Args>
void bail(const char *fmt, Args &&...args) {
    fmt::print(stderr, fmt, std::forward<Args>(args)...);
    std::exit(1);
}

TEST_CASE("Appender", "[appender]") {
    duckdb_database db;
    duckdb_connection con;
    duckdb_result result;
    REQUIRE(duckdb_open(nullptr, &db) == DuckDBSuccess);
    REQUIRE(duckdb_connect(db, &con) == DuckDBSuccess);

    SECTION("Struct") {
        REQUIRE(duckdb_query(con,
                             "CREATE TABLE a(i STRUCT(a INTEGER, b INTEGER))",
                             nullptr) == DuckDBSuccess);
        REQUIRE(duckdb_query(con,
                             "INSERT INTO a VALUES ({a : 1, b : 2}), ({a : 3, "
                             "b : 4}), ({a : 5, b : 6})",
                             nullptr) == DuckDBSuccess);
        duckdb_query(con, "SELECT i.a FROM a", &result);
        REQUIRE(duckdb_value_uint64(&result, 0, 0) == 1);
        REQUIRE(duckdb_value_uint64(&result, 0, 1) == 3);
    }
    SECTION("Struct Appender") {
        REQUIRE(duckdb_query(con,
                             "CREATE TABLE a(i STRUCT(a INTEGER, b INTEGER))",
                             nullptr) == DuckDBSuccess);
        duckdb_appender appender;
        REQUIRE(duckdb_appender_create(con, nullptr, "a", &appender) ==
                DuckDBSuccess);
        
    }
}
