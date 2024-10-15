#include <duckdb.hpp>
#include <fmt/format.h>

#include <any>
#include <vector>

using namespace duckdb;

using vva = std::vector<std::vector<std::any>>;

vva getData(unique_ptr<MaterializedQueryResult> &result) {
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

int main() {
  // Initialize an in-memory DuckDB database
  DuckDB db(nullptr);
  Connection con(db);

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
  appender.Append<const char *>("Bob");
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

  for (auto &row : data) {
    for (auto &val : row) {
      if (val.type() == typeid(std::string)) {
        fmt::print("{}, ", std::any_cast<std::string>(val));
      } else {
        fmt::print("NULL, ");
      }
    }
    fmt::println("");
  }

  fmt::println("Done");

  return 0;
}