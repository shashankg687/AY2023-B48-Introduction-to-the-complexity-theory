import numpy as np

def birth(tau, M, c):
    """
    Get the change in number of molecules to each cell of matrix M 
    by birth,
    the propensity in each cell is 
    c
    """
    
    # Get the propensity 
    P = c

    # Get the change (positive cause of birth)
    Z = np.random.poisson(lam=tau*P, size=M.shape)
    
    return Z


def die(tau, M, c):
    """
    Get the change in number of molecules to each cell of matrix M 
    by death,
    the propensity in cell i is
    c * M_i
    """

    # Get the propensity
    P = c * M

    # Get the change (negative cause of death)
    Z = -1 * np.random.poisson(lam=tau*P)
    
    return Z


def react(tau, M_A, M_B, c):
    """
    Get the change in number of molecules to each cell of matrices
    M_A and M_B, respectively
    by the reaction of species A and B according to the equation:
    2A + B -> 3A
    where the propensity in cell i is
    c * M_A_i * (M_A_i - 1) * M_B_i
    """
    

    # Get the propensity
    P = c * M_A * (M_A - 1) * M_B

    # Get the change
    Z = np.random.poisson(lam=tau*P)
    
    # The change is plus one for A and minus one for B
    Z_A = 1 * Z
    Z_B = -1 * Z
    
    return Z_A, Z_B


def diffuse(tau, M, d):
    """
    Get the change in number of molecules to each cell of matrix M 
    by diffusion in each of four directions,
    the propensity in cell i is
    d * M_i
    """
    
    # Get the matrix of propensity functions (for each cell)
    P  = d * M
    
    # Get the amount diffused in each of four directions
    Ds = np.random.poisson(lam=tau*P, size=(4,) + M.shape)
    
    # Zero matrix (for calculating difference vector)
    Z = np.zeros(shape=M.shape, dtype=np.int16)
    
    ### 1. Take from top of matrix and give to bottom of matrix 
    # Make D equal to all of first of Ds except bottom row
    D = Ds[0]  # grab first direction (down)
    D = D[:-1,:]  # get top (index all except bottom row)
    Z[:-1,:] -= D  # subtract from top
    Z[1:,:] += D  # add to bottom

    ### 2. Take from bottom of matrix and give to top of matrix  
    # Make D equal to all of second of Ds except top row
    D = Ds[1]  # grab second direction (up)
    D = D[1:,:]  # grab bottom (index all except top row)
    Z[1:,:] -= D  # subtract from bottom
    Z[:-1,:] += D  # add to top

    ### 3. Take from left of matrix and give to right of matrix
    D = Ds[2]  # grab third direction (right)
    D = D[:,:-1]  # grab left
    Z[:,:-1] -= D  # subtract from left
    Z[:,1:] += D  # add to right

    ### 4. Take from right of matrix and give to left of matrix
    D = Ds[3]  # grab fourth direction (left)
    D = D[:,1:]  # grab right
    Z[:,1:] -= D  # subtract from right
    Z[:,:-1] += D  # add to left
    
    return Z



# Initialization


def initialize_movie(N_t, m, n, A_init, B_init):
    """
    Initializes the 2D grid for a movie with N_t time points,
    m rows, and n columns. And with initial A and B set to
    A_init and B_init.
    
    Initializes the parameters with signed 16-bit integer, which
    can go from -32_768 to 32_767.
    """    
    
    # Initialize the grid of cells for A and B populations
    shape = (N_t, m, n)  # index by time, row, column

    X_A = np.zeros(shape, dtype=np.int16)  # set A population at all times to zero
    X_A[0] += A_init  # add initial A population for time zero

    X_B = np.zeros(shape, dtype=np.int16)  # do the same as above for B...
    X_B[0] += B_init

    return X_A, X_B


# Calculation

def calculate_picture(tau, M_A, M_B, mu, beta, alpha, kappa, d_A, d_B):
    """
    Calculate the number of molecules in each cell of the A and B grids
    for time t+1.
    
    Note that unlike "calculate_movie" we cannot write directly to the array
    so we need to return it, this means the for loop will look different.
    """
    
    # Birth
    Z_A_birth = birth(tau, M=M_A, c=mu)
    Z_B_birth = birth(tau, M=M_B, c=beta)


    # Die
    Z_A_death = die(tau, M=M_A, c=alpha)


    # React
    Z_A_react, Z_B_react = react(tau, M_A, M_B, c=kappa)


    # Diffuse
    Z_A_diffusion = diffuse(tau, M=M_A, d=d_A)
    Z_B_diffusion = diffuse(tau, M=M_B, d=d_B)
    
    
    # Calculate next grid
    M_A_next = M_A + Z_A_birth + Z_A_death + Z_A_react + Z_A_diffusion
    M_B_next = M_B + Z_B_birth + Z_B_react + Z_B_diffusion
    
    return M_A_next, M_B_next


# Miscillaneous initialization if we don't care about the movie and only the final timepoint

def initialize_picture(m, n, A_init, B_init):
    """
    Initializes the 2D grid for a picture with,
    m rows, and n columns. And with initial A and B set to
    A_init and B_init.
    
    Initializes the parameters with signed 16-bit integer, which
    can go from -32_768 to 32_767.
    """    
    
    # Initialize the grid of cells for A and B populations
    shape = (m, n)  # index by row, column

    X_A = np.zeros(shape, dtype=np.int16)  # set A population to zero
    X_A += A_init  # add initial A population for time zero

    X_B = np.zeros(shape, dtype=np.int16)  # do the same as above for B...
    X_B += B_init

    return X_A, X_B

