# uncomment the next line if running in a notebook
# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, cos, sin


def do_analytic(k_0, m_0, x_0, v_0):

    w = sqrt(k_0 / m_0)
    x = x_0
    v = v_0

    x_list = []
    v_list = []

    for t in t_array:

        x_list.append(x)
        v_list.append(v)

        x = (1 / w) * sin(w * t)
        v = cos(w * t)

    # convert trajectory lists into arrays, so they can be sliced (useful for Assignment 2)
    x_array = np.array(x_list)
    v_array = np.array(v_list)
    return (x_array, v_array)


def do_integration(m_0, k_0, x_0, v_0, func):

    m = m_0
    k = k_0
    x = x_0
    v = v_0
    # initialise empty lists to record trajectories
    x_list = []
    v_list = []

    # Euler integration
    for t in t_array:

        # append last state to trajectories
        x_list.append(x)
        v_list.append(v)

        # calculate new position and velocity for next iteration
        if t == 0:
            a, x, v = do_euler(m, k, x, v)
        else:
            a, x, v = func(m, k, x, v, x_list[-2])

    # convert trajectory lists into arrays, so they can be sliced (useful for Assignment 2)
    x_array = np.array(x_list)
    v_array = np.array(v_list)
    return (x_array, v_array)


def do_euler(m, k, x, v, *argv):
    # calculate new position and velocity for next iteration
    a = -k * x / m
    x = x + dt * v
    v = v + dt * a
    return (a, x, v)


def do_verlet(m, k, x, v, *argv):
    px = x
    # calculate new position and velocity for next iteration
    a = -k * x / m
    x = 2 * x - argv[0] + (dt ** 2) * a
    v = (x - px) / dt
    return (a, x, v)


# mass, spring constant, initial position and velocity
m = 1
k = 1
x = 0
v = 1

# simulation time, timestep and time
t_max = 100
dt = 0.1
t_array = np.arange(0, t_max, dt)

eulers = do_integration(m, k, x, v, do_euler)
verlets = do_integration(m, k, x, v, do_verlet)
analytics = do_analytic(m, k, x, v)

# plot the position-time graph
plt.figure(1)
plt.clf()
plt.xlabel("time (s)")
plt.grid()
plt.plot(t_array, eulers[0], label="x (m)")
plt.plot(t_array, eulers[1], label="v (m/s)")
plt.plot(t_array, verlets[0], label="x (m) verlet")
plt.plot(t_array, verlets[1], label="v (m/s) verlet")
plt.plot(t_array, analytics[0], label="x (m) anayl")
plt.plot(t_array, analytics[1], label="v (m/s) anayl")
plt.legend()
plt.show()
