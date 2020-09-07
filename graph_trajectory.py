import numpy as np
import matplotlib.pyplot as plt

plt.figure(1)
plt.clf()
plt.xlabel("time (s)")
plt.grid()

integrators = ["euler", "verlet"]

for integrator in integrators:
    results = np.loadtxt(f"trajectories-{integrator}.txt")
    plt.plot(results[:, 0], results[:, 1], label=f"x (m) {integrator}")
    plt.plot(results[:, 0], results[:, 2], label=f"v (m/s) {integrator}") 

plt.legend()
plt.show()
