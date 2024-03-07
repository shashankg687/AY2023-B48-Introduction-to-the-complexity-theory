"""Simulate a reaction-diffusion system to generate Turing Patterns

This system described by a PDE called the FitzHugh–Nagumo equation.
It is evaluated here using finite difference methods taken from:
https://ipython-books.github.io/124-simulating-a-partial-differential
-equation-reaction-diffusion-systems-and-turing-patterns/
"""

import matplotlib.pyplot as plt

def laplacian(Z, dx):
    """Calculate laplacian of array Z
    
    Params:
    Z [Array] - Array of spatial data to compute the laplacian of
    dx [float] - Spatial step size for finite difference method
                     Should be small compared to the size of the array
    """
    Ztop = Z[0:-2, 1:-1]
    Zleft = Z[1:-1, 0:-2]
    Zbottom = Z[2:, 1:-1]
    Zright = Z[1:-1, 2:]
    Zcenter = Z[1:-1, 1:-1]
    return (Ztop + Zleft + Zbottom + Zright -
            4 * Zcenter) / dx**2

def show_patterns(U, ax=None):
    """Visual representation of Turing Pattern
    
    Params:
    U [Array] - Array of spatial data to plot"""
    ax.imshow(U, cmap=plt.cm.viridis,
              interpolation='bilinear',
              extent=[-1, 1, -1, 1])
    ax.set_axis_off()