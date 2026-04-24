#include <iostream>
#include <omp.h>
#include <vector>
#include <cstdio>
#include <cmath>
#include <fstream>
#include <random>
#include "force_velocity_position.h"

using namespace std;

int main(int argc, char* argv[]){
    
    int num_part = stoi(argv[1]);
    double dt = stod(argv[2]);
    double T = stod(argv[3]);    

    Bodies universe;
    universe.x.resize(num_part);
    universe.y.resize(num_part);
    universe.vx.resize(num_part);
    universe.vy.resize(num_part);
    universe.mass.resize(num_part); 

    random_device rd;
    mt19937 gen(rd());

    uniform_real_distribution<double> pos_dist(/*-200, 200*/-500, 500);
    uniform_real_distribution<double> vel_dist(-0.5, 0.5);
    uniform_real_distribution<double> mass_dist(1, 10);

    for(int i=0; i<num_part; ++i){
        double gen_x = pos_dist(gen);
        double gen_y = pos_dist(gen);
        double gen_vx = vel_dist(gen);
        double gen_vy = vel_dist(gen);
        double gen_mass = mass_dist(gen);

        universe.x[i] = gen_x;
        universe.y[i] = gen_y;
        universe.vx[i] = gen_vx;
        universe.vy[i] = gen_vy;
        universe.mass[i] = gen_mass;
    }

    ofstream outFile("punti_prova_progetto.csv");
    outFile << "T";
    for(int i=0; i<num_part; ++i){
        outFile << ",X" << i << ",Y" << i;
    }
    outFile << "\n";

    double start_time=omp_get_wtime();
     
    for(double i=0; i<=T; i+=dt){
        force_velocity_position(universe, dt);
        outFile << i;

        for(int j=0; j<num_part;++j){
            outFile << "," << universe.x[j] << "," << universe.y[j];
        }
        outFile << "\n";
    }
    
    outFile.close();
    double end_time=omp_get_wtime();

    printf("Tempo di esecuzione: %f \n", end_time-start_time);

    return 0;

}