#include <iostream>
#include <vector>
#include <cmath>
#include <Eigen/Dense>

const double G = 6.67430e-11; // Gravitational constant
const double dt = 0.1; // Time step

struct Body {
    Eigen::Vector3d position;
    Eigen::Vector3d velocity;
    double mass;
};

Eigen::MatrixXd calculateForces(const std::vector<Body>& bodies) {
    int n = bodies.size();
    Eigen::MatrixXd forces = Eigen::MatrixXd::Zero(n, 3);
    Eigen::MatrixXd positions(n, 3);
    Eigen::VectorXd masses(n);

    for (int i = 0; i < n; ++i) {
        positions.row(i) = bodies[i].position;
        masses(i) = bodies[i].mass;
    }

    for (int i = 0; i < n; ++i) {
        Eigen::MatrixXd diff = positions.rowwise() - positions.row(i);
        Eigen::VectorXd distanceSq = diff.rowwise().squaredNorm();
        distanceSq = distanceSq.unaryExpr([](double x) { return x > 0 ? x : 1e-10; });
        Eigen::VectorXd forceMagnitude = G * masses(i) * masses.array() / distanceSq.array();
        
        Eigen::MatrixXd forceVectors = diff.array().colwise() * (forceMagnitude.array() / distanceSq.array().sqrt());
        forces.row(i) = forceVectors.colwise().sum();
    }

    return forces;
}

void updateBodies(std::vector<Body>& bodies, const Eigen::MatrixXd& forces) {
    for (size_t i = 0; i < bodies.size(); ++i) {
        Eigen::Vector3d acceleration = forces.row(i) / bodies[i].mass;
        bodies[i].velocity += acceleration * dt;
        bodies[i].position += bodies[i].velocity * dt;
    }
}

int main() {
    std::vector<Body> bodies = {
        {{0, 0, 0}, {0, 0, 0}, 1e24},  // Sun
        {{1.5e11, 0, 0}, {0, 3e4, 0}, 6e24},  // Earth
        {{2.3e11, 0, 0}, {0, 2.4e4, 0}, 6.4e23}  // Mars
    };

    int numSteps = 1000;

    for (int step = 0; step < numSteps; ++step) {
        Eigen::MatrixXd forces = calculateForces(bodies);
        updateBodies(bodies, forces);

        // Print positions (only for demonstration, you might want to store or visualize this data)
        std::cout << "Step " << step << ":\n";
        for (const auto& body : bodies) {
            std::cout << body.position.transpose() << "\n";
        }
        std::cout << "\n";
    }

    return 0;
}