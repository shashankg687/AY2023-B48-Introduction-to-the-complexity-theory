"""Runs simulation of time and spatially dependant ODE model"""

from fipy import Grid1D, CellVariable, TransientTerm, DiffusionTerm, Viewer
from gif_creator import create_gif
from builtins import range

h = 1

D_A, D_B = 1e-5/(2*h**2), 1e-3/(2*h**2)
alpha = 0.02
beta = 192000 * h**3
mu = 64000 * h**3
kappa = 2.44e-16 * h**-6
A_0, B_0 = 12800000, 4882812.5 # Should be defined as floats

nx = 100
dx = 1.1

time_step = 0.2
step_num, plot_num = 100, 20  # Plot num should be less than step num
delete_images = True  # Boolean to delete images after running

m = Grid1D(dx=dx, nx=nx)

v0 = CellVariable(name = "Concentration of A", mesh=m, hasOld=True, value=A_0)
v1 = CellVariable(name = "Concentration of B", mesh=m, hasOld=True, value=B_0)

eqn0 = TransientTerm(var=v0) == mu - alpha * v0 + kappa * v0**2 * v1 + DiffusionTerm(D_A, var=v0) 
eqn1 = TransientTerm(var=v1) == beta - kappa * v0**2 * v1 +  DiffusionTerm(D_B, var=v1)

eqn = eqn0 & eqn1

vi = Viewer((v0, v1), datamin=0, datamax= 1.1*A_0)
vi.axes.set_xlabel('x position (mm)')
vi.axes.set_ylabel('Concentration')

plotting_steps  = range(0, step_num, int(step_num/plot_num))
for step in range(step_num):
    v0.updateOld()
    v1.updateOld()
    eqn.solve(dt=time_step)
    if step in plotting_steps:
        vi.plot(f"Images/Spatial_ODE/Line1D_{step:04d}.png")
        for txt in vi.axes.texts:
            txt.set_visible(False)
        vi.axes.text(0.7 * dx * nx, 0.9 * A_0, f'Time = {step * time_step:.2f} s')
        
create_gif("Images/Spatial_ODE/Line1D", delete_images)