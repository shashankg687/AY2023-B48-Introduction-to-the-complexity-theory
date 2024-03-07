"""Plot a reaction-diffusion system to generate Turing Patterns

This system described by a PDE called the FitzHugh–Nagumo equation.
It is evaluated here using finite difference methods taken from:
https://ipython-books.github.io/124-simulating-a-partial-differential
-equation-reaction-diffusion-systems-and-turing-patterns/
"""

import numpy as np
import matplotlib.pyplot as plt
from finite_difference import laplacian, show_patterns
from gif_creator import create_gif

a = 2.8e-4
b = 5e-3
tau = .1
k = -.005

size = 100  # size of the 2D grid
dx = 2. / size  # space step

T = 10.0  # total time
dt = .001  # time step
n = int(T / dt)  # number of iterations
plot_num = 10

U = np.random.rand(size, size)
V = np.random.rand(size, size)

# U = np.ones((size, size)) + 0.01 * np.random.rand(size, size)
# V = np.ones((size, size)) + 0.01 * np.random.rand(size, size)

step_plot = n // plot_num
plot_count = 0
# Simulate the PDE with the finite difference method.
for i in range(n):
    # Compute the Laplacian of u and v.
    deltaU = laplacian(U, dx)
    deltaV = laplacian(V, dx)
    # Take the values of u and v inside the grid.
    Uc = U[1:-1, 1:-1]
    Vc = V[1:-1, 1:-1]
    # Update the variables.
    U[1:-1, 1:-1], V[1:-1, 1:-1] = \
        Uc + dt * (a * deltaU + Uc - Uc**3 - Vc + k),\
        Vc + dt * (b * deltaV + Uc - Vc) / tau
    # Neumann/zero flux conditions: derivatives at the edges
    # are null.
    for Z in (U, V):
        Z[0, :] = Z[1, :]
        Z[-1, :] = Z[-2, :]
        Z[:, 0] = Z[:, 1]
        Z[:, -1] = Z[:, -2]

    if i % step_plot == 0 and i < plot_num * step_plot:
        plot_count += 1
        plt.imshow(U, cmap=plt.cm.viridis,
              interpolation='bilinear',
              extent=[-1, 1, -1, 1])
        plt.title(f'$t={i * dt:.2f}$')
        plt.savefig(f"Images/Spatial_ODE/Turing_Evolution_Const2_{plot_count:04d}.png")
        #plt.show()
        
create_gif("Images/Spatial_ODE/Turing_Evolution_Const2")

fig, ax = plt.subplots(1, 1, figsize=(8, 8))
show_patterns(U, ax=ax)
plt.title(f'$t={i * dt:.2f}$')
plt.savefig("Images/Turing_Final_State.png")
plt.show()


