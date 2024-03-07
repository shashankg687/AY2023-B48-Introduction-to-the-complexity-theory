"""Runs simulation of time dependant ODE model"""

import numpy as np
import matplotlib.pyplot as plt
from ode_simulator import solve_schnakenberg

N_STEPS = int(1e3); STEP_SIZE = 0.005
INITIAL_COND = [0,1]  # Starting value of [A, B]
A_PROD, B_PROD = 1, 1  # Initial production rates
t_steps = np.linspace(0, N_STEPS * STEP_SIZE, N_STEPS)

time, state = solve_schnakenberg(t_max  = N_STEPS * STEP_SIZE, \
    y_init = INITIAL_COND, rates = [A_PROD, B_PROD], t_eval = t_steps)

plt.plot(time, state[0], label = 'A'); plt.plot(time, state[1], label = 'B')
plt.xlabel('Time (t)'); plt.ylabel('Concentration')
plt.title('Schnakenberg System - Time Evolution'); plt.legend()
plt.savefig('Images/Schnakenberg_time_evolution.png'); plt.show()