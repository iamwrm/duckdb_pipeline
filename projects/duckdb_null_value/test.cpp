#include "duckdb/common/types.hpp"
#include "fmt/base.h"
#include <any>
#include <cstdint>

#include <catch2/catch_test_macros.hpp>
#include <duckdb.hpp>
#include <fmt/format.h>

using namespace duckdb;

using vva = std::vector<std::vector<std::any>>;

vva getData(unique_ptr<MaterializedQueryResult>& result)
{
    vva ret;
    for (idx_t i = 0; i < result->RowCount(); i++) {
        std::vector<std::any> row;
        for (idx_t j = 0; j < result->ColumnCount(); j++) {
            auto val = result->GetValue(j, i);
            if (val.IsNull()) {
                row.push_back(std::any());
            } else {
                row.push_back(val.ToString());
            }
        }
        ret.push_back(row);
    }
    return ret;
};

void printData(vva& data)
{
    for (auto& row : data) {
        for (auto& val : row) {
            if (val.type() == typeid(std::string)) {
                fmt::print("{}, ", std::any_cast<std::string>(val));
            } else {
                fmt::print("NULL, ");
            }
        }
        fmt::println("");
    }
}

TEST_CASE("Appender", "[appender]")
{
    DuckDB db(nullptr);
    Connection con(db);

    auto print_result = [](auto& con, auto& query,
                            const std::string& comment = "") {
        fmt::println("Query: {} \n Comment: {}", query, comment);
        auto result = con.Query(query);
        fmt::println("{}", result->ToString());
    };

    SECTION("Appender null value")
    {
        // Create a sample table with nullable columns
        con.Query("CREATE TABLE persons(id INTEGER, name VARCHAR, age INTEGER)");

        duckdb::Appender appender(con, "persons");

        // Insert rows, including NULL values
        appender.AppendRow(1, "Alice", 30);
        appender.AppendRow(2, "123", 25);
        appender.AppendRow(3, "Charlie", 0);
        appender.AppendRow(4, nullptr, 10);

        appender.BeginRow();
        appender.Append<int32_t>(1);
        appender.Append<const char*>("Bob");
        appender.Append<int32_t>(20);
        appender.EndRow();

        appender.BeginRow();
        appender.Append<int32_t>(1);
        appender.AppendDefault();
        appender.Append<int32_t>(20);
        appender.EndRow();

        appender.Flush();

        // Query the table to verify the inserted data
        auto result = con.Query("SELECT * FROM persons");

        fmt::println("{}", result->ToString());

        auto data = getData(result);
        printData(data);
    }

    SECTION("query on nested struct")
    {
        auto result = con.Query(R"(
            SELECT 
                array_value(1, 2, 3),
                array_value(4, 5, 6),
                {'key1': 'value1', 'key2': 42}
        )");
        fmt::println("{}", result->ToString());

        fmt::println("Start printing array data");
        for (idx_t i = 0; i < result->RowCount(); i++) {
            for (idx_t j = 0; j < result->ColumnCount(); j++) {
                Value val = result->GetValue(j, i);
                if (val.IsNull()) {
                    fmt::print("NULL");
                } else {
                    fmt::print("{}  |  ", val.ToString());

                    // If this is an array, print the elements
                }
            }
        }

        fmt::println("");
    }
    SECTION("Stream result")
    {
        con.Query("CREATE TABLE a(i INTEGER)");
        con.Query("INSERT INTO a VALUES (12), (13), (14)");

        std::unique_ptr<PreparedStatement> prepare = con.Prepare("SELECT count(*) FROM a WHERE i = $1");

        std::unique_ptr<QueryResult> result = prepare->Execute(12);

        if (result->type == QueryResultType::STREAM_RESULT) {
            StreamQueryResult& stream = (StreamQueryResult&)*result;
            fmt::println("Stream result");
            // result = stream.Materialize();
            // fmt::println("Materialized result");
            auto fetch_result = stream.Fetch();
            fmt::println("{}", fetch_result->ToString());
        }
    }
    SECTION("Appender LIST")
    {
        con.Query("CREATE TABLE a(i INTEGER[])");
        // INSERT using string
        con.Query("INSERT INTO a VALUES ([1, 2, 3]), ([4, 5, 6]), ([7, 8, 9])");

        print_result(con, "SELECT * FROM a");

        // create a new appender
        duckdb::Appender appender(con, "a");
        appender.AppendRow(duckdb::Value::LIST({ 1, 2, 3 }));
        appender.AppendRow(duckdb::Value::LIST({ 4, 5, 6 }));
        appender.AppendRow(duckdb::Value::LIST({ 7, 8, 9 }));
        appender.Flush();

        print_result(con, "SELECT * FROM a");
    }

    SECTION("Appender STRUCT")
    {
        con.Query("CREATE TABLE a(i STRUCT(a INTEGER, b INTEGER))");
        con.Query("INSERT INTO a VALUES ({a : 1, b : 2}), ({a : 3, b : 4}), ({a : "
                  "5, b : 6})");

        print_result(con, "SELECT * FROM a");

        auto result = con.Query("SELECT * FROM a");
        Value value = result->GetValue(0, 0);
        fmt::println("{}", value.type().ToString());
        fmt::println("{}", value.ToString());
    }

    SECTION("Appender STRUCT nested")
    {
        con.Query("CREATE TABLE a(i STRUCT(a INTEGER, b INTEGER, c STRUCT(d INTEGER, e INTEGER)))");
        con.Query(R"(
            INSERT INTO a VALUES 
                ({a : 1, b : 2, c : {d : 3, e : 4}}), 
                ({a : 5, b : 6, c : {d : 7, e : 8}}), 
                ({a : 9, b : 10, c : {d : 11, e : 12}})
        )");

        print_result(con, "SELECT * FROM a");

        auto result = con.Query("SELECT * FROM a");
        Value value = result->GetValue(0, 0);
        fmt::println("{}", value.type().ToString());
        fmt::println("{}", value.ToSQLString());

        auto children = duckdb::StructValue::GetChildren(value);
        int i = 0;
        for (auto& child : children) {
            if (child.type().IsNested()) {
                fmt::println("Nested type: {}", child.type().ToString());
            }
            auto name = duckdb::StructType::GetChildName(value.type(), i);
            auto type = duckdb::StructType::GetChildType(value.type(), i);

            fmt::println("{}: {} = {}", name, type.ToString(), child.ToString());
            i++;
        }
    }
    SECTION("nested type in c api")
    {
    }
}
