package main

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/marcboeker/go-duckdb"
)

func main() {
	// Connect to DuckDB
	db, err := sql.Open("duckdb", "")
	if err != nil {
		log.Fatal("Error connecting to DuckDB:", err)
	}
	defer db.Close()

	// Create a table from the CSV file
	_, err = db.Exec(`
		CREATE TABLE test AS 
		SELECT * FROM read_csv_auto('test.csv')
	`)
	if err != nil {
		log.Fatal("Error creating table:", err)
	}

	// Query the data
	rows, err := db.Query("SELECT * FROM test")
	if err != nil {
		log.Fatal("Error querying data:", err)
	}
	defer rows.Close()

	// Print results
	for rows.Next() {
		var id int
		var name string
		if err := rows.Scan(&id, &name); err != nil {
			log.Fatal("Error scanning row:", err)
		}
		fmt.Printf("in Go, ID: %d, Name: %s\n", id, name)
	}

	if err = rows.Err(); err != nil {
		log.Fatal("Error iterating rows:", err)
	}
} 