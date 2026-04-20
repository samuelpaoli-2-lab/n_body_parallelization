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

/*void force_velocity_position(Bodies& body, double dt){
    int n = body.x.size();
    const double G = 1;//6.67430e-11;
    double sic = 1e-9;
    const int b = 64;
    #pragma omp parallel shared(body, n, dt, G, sic, b) default(none)
    {
        #pragma omp for schedule(runtime)
        for(int ii=0; ii<n; ii+=b){
            int i_max = (ii + b < n) ? ii + b : n;

            double block_fx[b] = {0.0};
            double block_fy[b] = {0.0};

            for(int jj=0; jj<n; jj+=b){

                int j_max = (jj + b < n) ? jj + b : n;

                for(int i = ii; i < i_max; ++i){

                    double xi = body.x[i];
                    double yi = body.y[i];
                    double mi = body.mass[i];

                    double fx = 0.0;
                    double fy = 0.0;

                    #pragma omp simd reduction(+:fx, fy)
                    for(int j=jj; j<j_max; ++j){

                        double dx = body.x[j] - xi;
                        double dy = body.y[j] - yi;

                        double r2 = dx*dx + dy*dy + sic;
                        double inv_dist = 1.0 / sqrt(r2); 
                        double inv = inv_dist * inv_dist * inv_dist;

                        double f = (G * mi * body.mass[j])*inv;

                        fx += f * dx;
                        fy += f * dy;
                    }

                    block_fx[i-ii]+=fx;
                    block_fy[i-ii]+=fy;

                }
            }
            for(int i = ii; i < i_max; ++i){
                body.vx[i] += (block_fx[i-ii]/body.mass[i]) * dt;
                body.vy[i] += (block_fy[i-ii]/body.mass[i]) * dt;  
            }
        }
        #pragma omp for nowait
            for(int i=0; i<n; ++i){
                body.x[i] += body.vx[i] * dt;
                body.y[i] += body.vy[i] * dt;
            }
    }
}*/
void force_velocity_position(Bodies& body, double dt) {
    int n = body.x.size();
    const double sic = 1e-9;
    
    // Vettori per accumulare le forze globali totali
    vector<double> total_fx(n, 0.0);
    vector<double> total_fy(n, 0.0);
    
    // Estraiamo i puntatori grezzi perché la sintassi di OpenMP li preferisce
    double* p_fx = total_fx.data();
    double* p_fy = total_fy.data();

    // FASE 1: Calcolo triangolare (Terza Legge di Newton)
    // Usiamo la riduzione sull'array: OpenMP gestisce la memoria locale per i thread!
    // Usiamo runtime così puoi continuare a pilotarlo da Makefile con dynamic.
    #pragma omp parallel for schedule(runtime) reduction(+: p_fx[:n], p_fy[:n]) default(none) shared(body, n, sic)
    for (int i = 0; i < n; ++i) {
        double xi = body.x[i];
        double yi = body.y[i];
        double mi = body.mass[i];

        // ECCO LA MAGIA: Iniziamo da j = i + 1. Calcoliamo solo metà delle coppie!
        for (int j = i + 1; j < n; ++j) {
            double dx = body.x[j] - xi;
            double dy = body.y[j] - yi;

            double r2 = dx * dx + dy * dy + sic;
            double inv_dist = 1.0 / sqrt(r2);
            double inv = inv_dist * inv_dist * inv_dist;

            double f = (mi * body.mass[j]) * inv;
            double fx_ij = f * dx;
            double fy_ij = f * dy;

            // AZIONE: Aggiungiamo la forza alla particella i
            p_fx[i] += fx_ij;
            p_fy[i] += fy_ij;
            
            // REAZIONE: Sottraiamo la STESSA forza alla particella j
            // Sicuro grazie alla riduzione su array di OpenMP!
            p_fx[j] -= fx_ij;
            p_fy[j] -= fy_ij;
        }
    }

    // FASE 2: Aggiornamento finale di velocità e posizioni
    // Questo ciclo è leggerissimo e perfettamente lineare
    #pragma omp parallel for schedule(static) default(none) shared(body, total_fx, total_fy, dt, n)
    for (int i = 0; i < n; ++i) {
        body.vx[i] += (total_fx[i] / body.mass[i]) * dt;
        body.vy[i] += (total_fy[i] / body.mass[i]) * dt;
        
        body.x[i] += body.vx[i] * dt;
        body.y[i] += body.vy[i] * dt;
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