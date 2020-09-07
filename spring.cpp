#include <fstream>
#include <iostream>
#include <vector>

#define SIMULATION_TIME 100

void integrate(struct Integrator* integrator, double dt);
void do_euler(struct Integrator* integrator, double dt);
void do_verlet(struct Integrator* integrator, double dt, double ppx);

using namespace std;

struct Integrator {
  double m;
  double k;
  double x_0;
  double v_0;
  vector<double> t_list;
  vector<double> x_list;
  vector<double> v_list;

  // temp vars to be stored in the struct for calcs
  double a;
  double x;
  double v;

  // config
  bool isVerlet;
};

void integrate(struct Integrator* integrator, double dt) {
  // Euler integration
  double t;
  integrator->x = integrator->x_0;
  integrator->v = integrator->v_0;
  for (t = 0; t <= SIMULATION_TIME; t = t + dt) {
    // append current state to trajectories
    double ppx;
    if (!integrator->x_list.empty()) {
      ppx = integrator->x_list.back();
    }

    integrator->t_list.push_back(t);
    integrator->x_list.push_back(integrator->x);
    integrator->v_list.push_back(integrator->v);

    if (integrator->x_list.empty() && integrator->isVerlet) {
      do_euler(integrator, dt);
    } else if (integrator->isVerlet) {
      do_verlet(integrator, dt, ppx);
    } else {
      do_euler(integrator, dt);
    }
  }
}

void do_euler(struct Integrator* integrator, double dt) {
  // calculate new position and velocity
  struct Integrator* i = integrator;
  i->a = -i->k * i->x / i->m;
  i->x = i->x + dt * i->v;
  i->v = i->v + dt * i->a;
};

void do_verlet(struct Integrator* integrator, double dt, double ppx) {
  // calculate new position and velocity
  struct Integrator* i = integrator;
  i->a = -i->k * i->x / i->m;
  double px = i->x;
  i->x = 2 * i->x - ppx + (dt * dt) * i->a;
  i->v = (i->x - px) / dt;
};

void save_trajectory(struct Integrator* integrator) {
  // Write the trajectories to file
  ofstream fout;
  if (integrator->isVerlet) {
    fout.open("trajectories-verlet.txt");

  } else {
    fout.open("trajectories-euler.txt");
  }
  if (fout) {  // file opened successfully
    for (int i = 0; i < integrator->t_list.size(); i = i + 1) {
      fout << integrator->t_list[i] << ' ' << integrator->x_list[i] << ' '
           << integrator->v_list[i] << endl;
    }
  } else {  // file did not open successfully
    cout << "Could not open trajectory file for writing" << endl;
  }
}

int main() {
  // declare variables
  struct Integrator euler_integrator;
  struct Integrator verlet_integrator;

  // mass, spring constant, initial position and velocity
  euler_integrator.m = 1;
  euler_integrator.k = 1;
  euler_integrator.x_0 = 0;
  euler_integrator.v_0 = 1;
  euler_integrator.isVerlet = false;

  verlet_integrator.m = 1;
  verlet_integrator.k = 1;
  verlet_integrator.x_0 = 0;
  verlet_integrator.v_0 = 1;
  verlet_integrator.isVerlet = true;

  integrate(&euler_integrator, 0.1);
  integrate(&verlet_integrator, 0.1);

  save_trajectory(&euler_integrator);
  save_trajectory(&verlet_integrator);
}
