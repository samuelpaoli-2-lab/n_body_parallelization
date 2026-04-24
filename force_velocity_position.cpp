#include "force_velocity_position.h"
#include <cmath>
#include <omp.h>

void force_velocity_position(Bodies& body, double dt) {
    int n = body.x.size();
    const double sic = 1e-9;
    
    vector<double> total_fx(n, 0.0);
    vector<double> total_fy(n, 0.0);
    
    double* p_fx = total_fx.data();
    double* p_fy = total_fy.data();

    #pragma omp parallel for schedule(runtime) reduction(+: p_fx[:n], p_fy[:n]) default(none) shared(body) firstprivate(n, sic)
    for (int i = 0; i < n; ++i) {
        double xi = body.x[i];
        double yi = body.y[i];
        double mi = body.mass[i];

        double fx_i_local = 0.0;
        double fy_i_local = 0.0;

        #pragma omp simd reduction(+: fx_i_local, fy_i_local)
        for (int j = i + 1; j < n; ++j) {
            double dx = body.x[j] - xi;
            double dy = body.y[j] - yi;

            double r2 = dx * dx + dy * dy + sic;
            double inv_dist = 1.0 / sqrt(r2);
            double inv = inv_dist * inv_dist * inv_dist;

            double f = (mi * body.mass[j]) * inv;
            double fx_ij = f * dx;
            double fy_ij = f * dy;

            fx_i_local += fx_ij;
            fy_i_local += fy_ij;
                
            p_fx[j] -= fx_ij;
            p_fy[j] -= fy_ij;
            }

        p_fx[i] += fx_i_local;
        p_fy[i] += fy_i_local;
    }
    

    #pragma omp parallel for default(none) shared(body, total_fx, total_fy) firstprivate(dt, n)
    for (int i = 0; i < n; ++i) {
        body.vx[i] += (total_fx[i] / body.mass[i]) * dt;
        body.vy[i] += (total_fy[i] / body.mass[i]) * dt;
        
        body.x[i] += body.vx[i] * dt;
        body.y[i] += body.vy[i] * dt;
    }
    
}