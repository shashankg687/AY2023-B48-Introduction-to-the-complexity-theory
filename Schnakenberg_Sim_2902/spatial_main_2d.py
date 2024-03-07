"""Runs simulation of time and spatially dependant ODE model

Plots one concentration variable at subsequent timepoints and then converts 
these into a .gif, optionally deleting the image files afterwards
"""

from fipy import Grid2D, CellVariable, TransientTerm, DiffusionTerm, Viewer, GaussianNoiseVariable
from gif_creator import create_gif

h = 25e-3

D_A, D_B = 1e-5/(2*h**2), 1e-3/(2*h**2)
alpha = 0.02
beta = 192000 * h**3
mu = 64000 * h**3
kappa = 2.44e-16 * h**-6
A_0, B_0 = 200.0, 75.0  # Should be defined as floats

nx = 100
dx = 1.1
m = Grid2D(dx=dx, dy=dx, nx=nx, ny=nx)
volumes = CellVariable(mesh=m, value=m.cellVolumes)

time_step = 0.2
step_num, plot_num = 100, 20  # Plot num should be less than step num

delete_images = True  # Boolean to delete images after running
random_initial_state = True  # Boolean to determine whether initial state has gaussian noise

if random_initial_state:
    v0 = GaussianNoiseVariable(name = "Concentration of A", mesh=m, hasOld=True,
                               mean=A_0,variance=A_0 / volumes)
    v1 = GaussianNoiseVariable(name = "Concentration of B", mesh=m, hasOld=True,
                               mean=B_0,variance=B_0 / volumes)
else:
    v0 = CellVariable(name = "Concentration of A", mesh=m, hasOld=True, value=A_0)
    v1 = CellVariable(name = "Concentration of B", mesh=m, hasOld=True, value=B_0)
plot_var = v0  # CHANGE THIS TO V0 OR V1 TO DETERMINE WHICH VARIABLE IS PLOTTED

eqn0 = TransientTerm(var=v0) == mu - alpha * v0 + kappa * v0**2 * v1 + DiffusionTerm(D_A, var=v0) 
eqn1 = TransientTerm(var=v1) == beta - kappa * v0**2 * v1 +  DiffusionTerm(D_B, var=v1)
eqn = eqn0 & eqn1

viewer = Viewer(vars=plot_var) #, datamin=0, datamax= A_0)
viewer.axes.set_xlabel('x position (mm)')
viewer.axes.set_ylabel('y position (mm)')

plotting_steps  = range(0, step_num, int(step_num/plot_num))
for step in range(step_num):
    v0.updateOld()
    v1.updateOld()
    eqn.solve(dt=time_step)
    if step in plotting_steps:
        viewer.plot(f"Images/Spatial_ODE/Mesh2D_{step:04d}.png")
        for txt in viewer.axes.texts:
            txt.set_visible(False)
        viewer.axes.text(0.7*dx*nx, 0.93*dx*nx, f'Time = {step * time_step:.2f} s',
                bbox={'facecolor': 'white', 'alpha': 0.8, 'pad': 2.5})

create_gif("Images/Spatial_ODE/Mesh2D", delete_images)

