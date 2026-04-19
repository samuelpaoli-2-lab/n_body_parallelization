#include <iostream>
#include <omp.h>
#include <vector>
#include <cstdio>
#include <cmath>
#include <fstream>
#include <random>

using namespace std;

struct Bodies{
    vector<double> x, y;
    vector<double> vx, vy;
    vector<double> mass;
};

void force_velocity_position(Bodies& body, double dt){
    int n = body.x.size();
    const double G = 1/*6.67430e-11*/;
    double sic = 1e-9;
    #pragma omp parallel shared(body, n, dt, G, sic) default(none)
    {
        #pragma omp for schedule(runtime)
        for(int i=0; i<n; ++i){
            double fx = 0, fy = 0;
            double xi = body.x[i];
            double yi = body.y[i];
            double mi = body.mass[i];

            #pragma omp simd reduction(+:fx, fy)
            for(int j=0; j<n; ++j){

                double dx = body.x[j] - xi;
                double dy = body.y[j] - yi;

                double dist = sqrt(dx*dx + dy*dy + sic);
                double inv = 1.0/(dist*dist*dist);

                double f = (G * mi * body.mass[j])*inv;

                fx += f * dx;
                fy += f * dy;
            }

            body.vx[i] += (fx/mi) * dt;
            body.vy[i] += (fy/mi) * dt;
        }

        #pragma omp for nowait
        for(int i=0; i<n; ++i){
            body.x[i] += body.vx[i] * dt;
            body.y[i] += body.vy[i] * dt;
        }
    }
}

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

    /*ofstream outFile("punti_prova_progetto.csv");
    outFile << "T";
    for(int i=0; i<num_part; ++i){
        outFile << ",X" << i << ",Y" << i;
    }
    outFile << "\n";*/

    double start_time=omp_get_wtime();
     
    for(double i=0; i<=T; i+=dt){
        force_velocity_position(universe, dt);
        /*outFile << i;

        for(int j=0; j<num_part;++j){
            outFile << "," << universe.x[j] << "," << universe.y[j];
        }
        outFile << "\n";*/
    }
    
    //outFile.close();
    double end_time=omp_get_wtime();

    printf("Tempo di esecuzione: %f \n", end_time-start_time);

    return 0;

}