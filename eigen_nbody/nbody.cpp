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

Eigen::Vector3d calculateForce(const Body& body1, const Body& body2) {
    Eigen::Vector3d r = body2.position - body1.position;
    double distance = r.norm();
    double forceMagnitude = G * body1.mass * body2.mass / (distance * distance);
    return forceMagnitude * r.normalized();
}

void updatePositionAndVelocity(Body& body, const Eigen::Vector3d& force) {
    Eigen::Vector3d acceleration = force / body.mass;
    body.velocity += acceleration * dt;
    body.position += body.velocity * dt;
}

int main() {
    std::vector<Body> bodies = {
        {{0, 0, 0}, {0, 0, 0}, 1e24},  // Sun
        {{1.5e11, 0, 0}, {0, 3e4, 0}, 6e24},  // Earth
        {{2.3e11, 0, 0}, {0, 2.4e4, 0}, 6.4e23}  // Mars
    };

    int numSteps = 1000;

    for (int step = 0; step < numSteps; ++step) {
        for (size_t i = 0; i < bodies.size(); ++i) {
            Eigen::Vector3d totalForce(0, 0, 0);
            
            for (size_t j = 0; j < bodies.size(); ++j) {
                if (i != j) {
                    totalForce += calculateForce(bodies[i], bodies[j]);
                }
            }
            
            updatePositionAndVelocity(bodies[i], totalForce);
        }

        // Print positions (only for demonstration, you might want to store or visualize this data)
        std::cout << "Step " << step << ":\n";
        for (const auto& body : bodies) {
            std::cout << body.position.transpose() << "\n";
        }
        std::cout << "\n";
    }

    return 0;
}