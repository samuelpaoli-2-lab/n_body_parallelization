#pragma once
#include <vector>

using namespace std;

struct Bodies{
    vector<double> x, y;
    vector<double> vx, vy;
    vector<double> mass;
};

void force_velocity_position(Bodies& body, double dt);