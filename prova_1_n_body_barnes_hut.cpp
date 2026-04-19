#include <chrono>
#include <cmath>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <random>
#include <vector>

using namespace std;

struct Body {
    double x, y;
    double vx, vy;
    double mass;
};

struct Quad {
    double cx, cy; // center
    double hw, hh; // half width/half height

    bool contains(double x, double y) const {
        return x >= cx - hw && x <= cx + hw && y >= cy - hh && y <= cy + hh;
    }
};

struct Node {
    Quad region;
    double mass;
    double com_x, com_y;
    int body_index;
    int child[4];
    bool is_leaf;

    Node() : mass(0), com_x(0), com_y(0), body_index(-1), is_leaf(true) {
        child[0] = child[1] = child[2] = child[3] = -1;
    }
};

int get_quadrant(const Quad& q, double x, double y) {
    bool right = x >= q.cx;
    bool top = y >= q.cy;
    if (right) {
        return top ? 0 : 3; // NE, SE
    }
    return top ? 1 : 2; // NW, SW
}

Quad subdivide(const Quad& q, int idx) {
    double hw = q.hw / 2.0;
    double hh = q.hh / 2.0;
    switch (idx) {
        case 0: return {q.cx + hw, q.cy + hh, hw, hh}; // NE
        case 1: return {q.cx - hw, q.cy + hh, hw, hh}; // NW
        case 2: return {q.cx - hw, q.cy - hh, hw, hh}; // SW
        case 3: return {q.cx + hw, q.cy - hh, hw, hh}; // SE
        default: return q;
    }
}

int create_node(vector<Node>& nodes, const Quad& region) {
    nodes.emplace_back();
    nodes.back().region = region;
    return static_cast<int>(nodes.size()) - 1;
}

void insert_body(vector<Node>& nodes, int node_idx, int body_idx, const vector<Body>& bodies) {
    Node& node = nodes[node_idx];
    const Body& new_body = bodies[body_idx];

    if (node.body_index == -1 && node.is_leaf) {
        node.body_index = body_idx;
        node.mass = new_body.mass;
        node.com_x = new_body.x;
        node.com_y = new_body.y;
        return;
    }

    if (node.is_leaf) {
        int existing_body = node.body_index;
        node.body_index = -1;
        node.is_leaf = false;
        for (int i = 0; i < 4; ++i) {
            Quad child_region = subdivide(node.region, i);
            node.child[i] = create_node(nodes, child_region);
        }
        // reinsert existing body
        insert_body(nodes, node.child[get_quadrant(node.region, bodies[existing_body].x, bodies[existing_body].y)], existing_body, bodies);
    }

    int quadrant = get_quadrant(node.region, new_body.x, new_body.y);
    insert_body(nodes, node.child[quadrant], body_idx, bodies);

    // update center of mass / total mass
    double total_mass = node.mass + new_body.mass;
    if (total_mass > 0) {
        node.com_x = (node.com_x * node.mass + new_body.x * new_body.mass) / total_mass;
        node.com_y = (node.com_y * node.mass + new_body.y * new_body.mass) / total_mass;
        node.mass = total_mass;
    }
}

void compute_force(const vector<Node>& nodes, int node_idx, const Body& body, double theta, double& fx, double& fy) {
    const Node& node = nodes[node_idx];
    if (node.mass == 0 || (node.is_leaf && node.body_index == -1)) {
        return;
    }

    double dx = node.com_x - body.x;
    double dy = node.com_y - body.y;
    double dist2 = dx * dx + dy * dy + 1e-9;
    double dist = sqrt(dist2);

    double s = node.region.hw * 2.0;
    if (node.is_leaf || s / dist < theta) {
        double inv = 1.0 / (dist2 * dist);
        double f = node.mass * inv;
        fx += f * dx;
        fy += f * dy;
        return;
    }

    for (int c = 0; c < 4; ++c) {
        if (node.child[c] != -1) {
            compute_force(nodes, node.child[c], body, theta, fx, fy);
        }
    }
}

Quad bounding_box(const vector<Body>& bodies) {
    double min_x = bodies[0].x, max_x = bodies[0].x;
    double min_y = bodies[0].y, max_y = bodies[0].y;
    for (size_t i = 1; i < bodies.size(); ++i) {
        min_x = min(min_x, bodies[i].x);
        max_x = max(max_x, bodies[i].x);
        min_y = min(min_y, bodies[i].y);
        max_y = max(max_y, bodies[i].y);
    }
    double cx = (min_x + max_x) / 2.0;
    double cy = (min_y + max_y) / 2.0;
    double hw = max(max_x - min_x, max_y - min_y) / 2.0;
    hw = max(hw, 1.0);
    return {cx, cy, hw * 1.1, hw * 1.1};
}

int main(int argc, char* argv[]) {
    if (argc < 4) {
        cerr << "Usage: " << argv[0] << " <num_part> <dt> <T>\n";
        return 1;
    }

    int num_part = stoi(argv[1]);
    double dt = stod(argv[2]);
    double T = stod(argv[3]);

    vector<Body> bodies(num_part);
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<double> pos_dist(-500.0, 500.0);
    uniform_real_distribution<double> vel_dist(-0.5, 0.5);
    uniform_real_distribution<double> mass_dist(1.0, 10.0);

    for (int i = 0; i < num_part; ++i) {
        bodies[i] = {pos_dist(gen), pos_dist(gen), vel_dist(gen), vel_dist(gen), mass_dist(gen)};
    }

    const double G = 1.0;
    const double theta = 0.5;
    auto start_time = chrono::high_resolution_clock::now();

    for (double t = 0.0; t <= T; t += dt) {
        Quad root_region = bounding_box(bodies);
        vector<Node> nodes;
        nodes.reserve(num_part * 4);
        int root = create_node(nodes, root_region);

        for (int i = 0; i < num_part; ++i) {
            insert_body(nodes, root, i, bodies);
        }

        vector<double> ax(num_part, 0.0);
        vector<double> ay(num_part, 0.0);

        for (int i = 0; i < num_part; ++i) {
            double fx = 0.0;
            double fy = 0.0;
            compute_force(nodes, root, bodies[i], theta, fx, fy);
            ax[i] = fx * G;
            ay[i] = fy * G;
        }

        for (int i = 0; i < num_part; ++i) {
            bodies[i].vx += ax[i] * dt / bodies[i].mass;
            bodies[i].vy += ay[i] * dt / bodies[i].mass;
            bodies[i].x += bodies[i].vx * dt;
            bodies[i].y += bodies[i].vy * dt;
        }
    }

    auto end_time = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = end_time - start_time;
    cout << "Barnes-Hut tempo di esecuzione: " << elapsed.count() << "\n";
    return 0;
}
