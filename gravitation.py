# uncomment the next line if running in a notebook
# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt


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
                a, x, v = do_euler(x, v, t)
            else:
                a, x, v = func(x, v, x_list[-2])

    return (x_list, v_list)


def do_euler(x, v, *argv):
    # calculate new position and velocity for next iteration
    mag_x = np.linalg.norm(x)
    a = (-G * M / (mag_x ** 2)) * (x / mag_x)
    x = x + dt * v
    v = v + dt * a
    return (a, x, v)


def do_verlet(x, v, *argv):
    px = x
    # calculate new position and velocity for next iteration
    mag_x = np.linalg.norm(x)
    a = (-G * M / (mag_x ** 2)) * (x / mag_x)
    x = 2 * x - argv[0] + (dt ** 2) * a
    v = (x - px) / dt
    return (a, x, v)


# mass, gravitational constant, initial position and velocity
M = 6.42 * 10 ** 23
G = 6.67 * 10 ** (-11)
MARS_RAD = 3386000
pos = [0, MARS_RAD + 30000, 0]
vel = [0, 0, 0]

# simulation time, timestep and time
t_max = 100
# critical value 1.7-1.8
dt = 0.1
t_array = np.arange(0, t_max, dt)

euler = do_integration(pos, vel, do_euler)
verlet = do_integration(pos, vel, do_verlet)

euler_mag = np.apply_along_axis(np.linalg.norm, 1, euler[0])
verlet_mag = np.apply_along_axis(np.linalg.norm, 1, verlet[0])

# plot the position-time graph
plt.figure(1)
plt.clf()
plt.xlabel("time (s)")
plt.ylabel("norm of x/v")
plt.grid()
plt.ticklabel_format(useOffset=False, style='plain')
# plt.ylim(bottom=-10, top=10)  set the ylim to bottom, top
plt.plot(t_array, euler_mag, label="x (m) euler")
plt.plot(t_array, verlet_mag, label="x (m) verlet")
plt.legend()
plt.show()
