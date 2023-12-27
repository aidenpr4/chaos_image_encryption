import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import cnames
from matplotlib import animation

# Logistic Map function
def logistic_map(r, x):
    return r * x * (1 - x)

# Parameters
r_values = np.linspace(1, 4, 10000)  # Range of 'r' values
x = 0.5  # Initial value of 'x'
iterations = 1000  # Number of iterations to discard (to reach a stable state)
plot_iterations = 500  # Number of iterations to plot

# Initialize lists to store values
x_values = []

# Generate bifurcation diagram data
for r in r_values:
    for _ in range(iterations):
        x = logistic_map(r, x)
    for _ in range(plot_iterations):
        x = logistic_map(r, x)
        x_values.append([r, x])

# Extract 'r' and 'x' values for plotting
r_values_plot = [item[0] for item in x_values]
x_values_plot = [item[1] for item in x_values]

# Plot the bifurcation diagram with thinner lines
plt.figure(figsize=(10, 9))
plt.scatter(r_values_plot, x_values_plot, s=0.0001, marker='.', c='blue')  # Adjust 's' parameter for thinner lines
plt.title("Bifurcation Diagram - Logistic Map")
plt.xlabel("r")
plt.ylabel("Value of x")
plt.xlim(1, 4)
plt.ylim(0, 1)

N_trajectories = 20

def lorentz_deriv(xyz, t0, sigma=10., beta=8./3, rho=28.0):
    """Compute the time-derivative of a Lorentz system."""
    return [sigma * (xyz[1] - xyz[0]), xyz[0] * (rho - xyz[2]) - xyz[1], xyz[0] * xyz[1] - beta * xyz[2]]

# Choose random starting points, uniformly distributed from -15 to 15
np.random.seed(1)
x0 = -15 + 30 * np.random.random((N_trajectories, 3))

# Solve for the trajectories
t = np.linspace(0, 4, 1000)
x_t = np.asarray([odeint(lorentz_deriv, x0i, t)
                  for x0i in x0])

# Set up figure & 3D axis for animation
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
ax.axis('off')

# choose a different color for each trajectory
colors = plt.cm.jet(np.linspace(0, 1, N_trajectories))

# set up lines and points
lines = sum([ax.plot([], [], [], '-', c=c)
             for c in colors], [])
pts = sum([ax.plot([], [], [], 'o', c=c)
           for c in colors], [])

# prepare the axes limits
ax.set_xlim((-25, 25))
ax.set_ylim((-35, 35))
ax.set_zlim((5, 55))

# set point-of-view: specified by (altitude degrees, azimuth degrees)
ax.view_init(30, 0)

# initialization function: plot the background of each frame
def init():
    for line, pt in zip(lines, pts):
        line.set_data([], [])
        line.set_3d_properties([])

        pt.set_data([], [])
        pt.set_3d_properties([])
    return lines + pts

# animation function.  This will be called sequentially with the frame number
def animate(i):
    # we'll step two time-steps per frame.  This leads to nice results.
    i = (2 * i) % x_t.shape[1]

    for line, pt, xi in zip(lines, pts, x_t):
        x, y, z = xi[:i].T
        line.set_data(x, y)
        line.set_3d_properties(z)

        pt.set_data(x[-1:], y[-1:])
        pt.set_3d_properties(z[-1:])

    ax.view_init(30, 0.3 * i)
    fig.canvas.draw()
    return lines + pts

# instantiate the animator.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=500, interval=30, blit=True)

# Save as mp4. This requires mplayer or ffmpeg to be installed
#anim.save('lorentz_attractor.mp4', fps=15, extra_args=['-vcodec', 'libx264'])

plt.show()

