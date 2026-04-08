#include <iostream>
#include <omp.h>
#include <vector>
#include <cstdio>
#include <cmath>
#include <fstream>
#include<random>

using namespace std;

struct Body{
    double x, y;
    double vx, vy;
    double mass;
};

void force_velocity_position(vector<Body>& body, double dt){
    int n = body.size();
    const double G = 1/*6.67430e-11*/;
    double sic = 1e-9;
    #pragma omp parallel shared(body, n, dt, G, sic) default(none)
    {

        #pragma omp for schedule(runtime)
        for(int i=0; i<n; ++i){
            double fx = 0, fy = 0;
            double xi = body[i].x;
            double yi = body[i].y;
            double mi = body[i].mass;

            #pragma omp simd reduction(+:fx, fy)
            for(int j=0; j<n; ++j){

                double dx = body[j].x - xi;
                double dy = body[j].y - yi;

                double dist = sqrt(dx*dx + dy*dy + sic);
                double inv = 1.0/(dist*dist*dist);

                double f = (G * mi * body[j].mass)*inv;

                fx += f * dx;
                fy += f * dy;
            }

            body[i].vx += (fx/mi) * dt;
            body[i].vy += (fy/mi) * dt;
        }

        #pragma omp for
        for(int i=0; i<n; ++i){
            body[i].x += body[i].vx * dt;
            body[i].y += body[i].vy * dt;
        }
    }
}

int main(int argc, char* argv[]){
    
    int num_part = stoi(argv[1]);
    double dt = stod(argv[2]);
    double T = stod(argv[3]);    

    vector <Body> universe; 

    random_device rd;
    mt19937 gen(rd());

    uniform_real_distribution<double> pos_dist(-200, 200);
    uniform_real_distribution<double> vel_dist(-0.5, 0.5);
    uniform_real_distribution<double> mass_dist(1, 10);

    for(int i=0; i<num_part; ++i){
        double gen_x = pos_dist(gen);
        double gen_y = pos_dist(gen);
        double gen_vx = vel_dist(gen);
        double gen_vy = vel_dist(gen);
        double gen_mass = mass_dist(gen);

        universe.push_back({gen_x, gen_y, gen_vx, gen_vy, gen_mass});
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
            outFile << "," << universe[j].x << "," << universe[j].y;
        }
        outFile << "\n";*/
    }
    
    //outFile.close();
    double end_time=omp_get_wtime();

    printf("Tempo di esecuzione: %f \n", end_time-start_time);

    return 0;

}