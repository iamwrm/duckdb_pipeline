#include <iostream>
#include <vector>
#include <cmath>
#include <duckdb.hpp>
#include <Eigen/Dense>

struct Body {
    int id;
    double x, y, z;
};

std::vector<Body> loadBodiesFromDuckDB(duckdb::Connection& conn) {
    std::vector<Body> bodies;
    auto result = conn.Query("SELECT id, x, y, z FROM bodies");
    
    for (auto& row : result) {
        bodies.push_back({
            row.GetValue<int>(0),
            row.GetValue<double>(1),
            row.GetValue<double>(2),
            row.GetValue<double>(3)
        });
    }
    
    return bodies;
}

void calculateDistances(const std::vector<Body>& bodies, duckdb::Connection& conn) {
    int n = bodies.size();
    Eigen::MatrixXd positions(n, 3);
    
    // Fill the positions matrix
    for (int i = 0; i < n; ++i) {
        positions.row(i) << bodies[i].x, bodies[i].y, bodies[i].z;
    }
    
    // Calculate pairwise squared distances
    Eigen::MatrixXd squared_distances = (
        positions.rowwise().replicate(n).colwise() - 
        positions.transpose().colwise().replicate(n)
    ).rowwise().squaredNorm();
    
    // Take the square root to get actual distances
    Eigen::MatrixXd distances = squared_distances.array().sqrt();
    
    // Store distances in DuckDB
    conn.Query("CREATE TABLE IF NOT EXISTS distances (body1_id INTEGER, body2_id INTEGER, distance DOUBLE)");
    
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            std::string query = "INSERT INTO distances (body1_id, body2_id, distance) VALUES (" +
                                std::to_string(bodies[i].id) + ", " +
                                std::to_string(bodies[j].id) + ", " +
                                std::to_string(distances(i, j)) + ")";
            conn.Query(query);
        }
    }
}

int main() {
    try {
        duckdb::DuckDB db(":memory:");
        duckdb::Connection conn(db);
        
        // Create and populate the bodies table
        conn.Query("CREATE TABLE bodies (id INTEGER, x DOUBLE, y DOUBLE, z DOUBLE)");
        conn.Query("INSERT INTO bodies VALUES (1, 0, 0, 0), (2, 1, 1, 1), (3, 2, 2, 2), (4, 3, 3, 3)");
        
        std::vector<Body> bodies = loadBodiesFromDuckDB(conn);
        calculateDistances(bodies, conn);
        
        // Verify results
        auto result = conn.Query("SELECT * FROM distances ORDER BY body1_id, body2_id");
        result->Print();
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}