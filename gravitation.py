# uncomment the next line if running in a notebook
# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt


def do_integration(x_0, v_0, func):

    x = np.array(x_0)
    v = np.array(v_0)

    # initialise empty lists to record trajectories
    x_list = np.array([x])
    v_list = np.array([v])

    for t in t_array:

        # append latest vals to trajectories, but skip first go
        if t != 0:
            x_list = np.append(x_list, [x], axis=0)
            v_list = np.append(v_list, [v], axis=0)

        if not (np.linalg.norm(x) <= MARS_RAD):

            # calculate new position and velocity for next iteration
            if t == 0:
                x, v = do_euler(x, v, t)
            else:
                x, v = func(x, v, x_list[-2])

    return (x_list, v_list)


def do_euler(x, v, *argv):
    # calculate new position and velocity for next iteration
    mag_x = np.linalg.norm(x)
    a = (-G * M / (mag_x ** 2)) * (x / mag_x)
    x = x + dt * v
    v = v + dt * a
    return (x, v)


def do_verlet(x, v, *argv):
    px = x
    # calculate new position and velocity for next iteration
    mag_x = np.linalg.norm(x)
    a = (-G * M / (mag_x ** 2)) * (x / mag_x)
    x = 2 * x - argv[0] + (dt ** 2) * a
    v = (x - px) / dt
    return (x, v)


def get_component(arr, axis, index):
    return np.apply_along_axis(lambda a_1d: a_1d[index], axis, arr)


def get_xy(arr):
    return (get_component(arr, 1, 0), get_component(arr, 1, 1))


# mass, gravitational constant, initial position and velocity
M = 6.42 * 10 ** 23
G = 6.67 * 10 ** (-11)
MARS_RAD = 3386000
HEIGHT_ABOVE_SURFACE = 30000
TOTAL_HEIGHT = MARS_RAD + HEIGHT_ABOVE_SURFACE
mag_vel_circ = sqrt(G * M / TOTAL_HEIGHT)
mag_vel_escape = sqrt(2) * mag_vel_circ
pos = [0, TOTAL_HEIGHT, 0]
vel = [mag_vel_circ, 0, 0]

# simulation time, timestep and time
t_max = 6000
# critical value 1.7-1.8
dt = 0.1
t_array = np.arange(0, t_max, dt)

euler = do_integration(pos, vel, do_euler)
verlet = do_integration(pos, vel, do_verlet)

# euler_mag = np.apply_along_axis(np.linalg.norm, 1, euler[0])
# verlet_mag = np.apply_along_axis(np.linalg.norm, 1, verlet[0])

euler_x, euler_y = get_xy(euler[0])
verlet_x, verlet_y = get_xy(verlet[0])

# plot the position-time graph
plt.figure(1, (6.4, 6.4))
plt.clf()
plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.grid()
plt.ticklabel_format(useOffset=False, style="plain")
# plt.ylim(bottom=-10, top=10)  set the ylim to bottom, top
plt.plot(euler_x, euler_y, label="euler")
plt.plot(verlet_x, verlet_y, label="verlet")
plt.legend()
plt.show()
