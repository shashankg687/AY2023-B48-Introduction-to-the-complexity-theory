""" Solves time dependant ODE model without spatial variation
"""

from scipy.integrate import solve_ivp


def ode_schnakenberg(t, y, a_prod, b_prod):
    """Derivatives to be called into solve_ivp
    
    This returns an array of derivatives y' = [A', B'], for a given
    state [A, B] at a time t. This is based on the classical 
    Schnakenberg system.

    Params:
    t [float] - the time at which the derivative is evaluated
    y [array] - the current state of the system, in the form [A, B]
    """

    return [y[0]**2 * y[1] - y[0] + a_prod, -y[0]**2 * y[1] + b_prod]


def solve_schnakenberg(t_max, t_min = 0, y_init = [0,0], rates = [0,0], t_eval = None):
    """Return solutions of Schnakenberg system
    
    Params:
    t_max [float] - the max time to be evaluated
    t_min [float] - the time of the initial state (default 0.0)
    y_init [list] - the initial values for the solver (default [0, 0])
    rates  [list] - the production rates of A and B (default [0, 0]
    """

    solution = solve_ivp(ode_schnakenberg, 
                         args = rates,  # Arguments for derivatives function
                         t_span = (t_min, t_max), 
                         t_eval = t_eval,
                         y0 = y_init,
                         method = 'RK45',
                         dense_output=True)
    return solution.t, solution.y


