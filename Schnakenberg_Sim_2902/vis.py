import numpy as np
import matplotlib.pyplot as plt
import imageio
import os



def catscan2png(M, filename, kind="X_A", window=10):
    
    picturepath = "Pictures/"
    picture_names = list()
    
    for z in np.arange(0, 1000, window):
        
        suffix =  "-catscan" + f"-{z}-" + kind
        
        plt.imshow(M, vmin=z, vmax=z+window)
        
        plt.xticks([])
        plt.yticks([])
        cb = plt.colorbar()
        
        picturename = picturepath + filename + suffix + ".png"
        picture_names.append(picturename)

        plt.tight_layout()
        plt.savefig(picturename, dpi=350)

        cb.remove()
        
    return picture_names



def movie2png(X, filename, kind="X_A", every=5_000, max_value=1000, movie_type="imshow", N_max=None):
    
    picturepath = "Pictures/"
    picture_names = list()
    
    N_t, m, n  = X.shape
    
    if N_max:
        N_t = N_max
    
    for t in np.arange(0, N_t, every):
        
        M = X[t]
        
        suffix = "-" + movie_type + f"-{t}-" + kind
        picturename = picturepath + filename + suffix + ".png"
        picture_names.append(picturename)
        
        if movie_type == "imshow":
            plot_imshow(M, picturename, vmin=0, vmax=max_value, save=True, dpi=350)
            
        if movie_type == "surface":
            plot_surface(M, picturename, zmin=0, zmax=max_value, save=True, dpi=350)
            
    return picture_names
            
    

def plot_imshow(M, picturename, vmin, vmax, save, dpi):
    
    plt.imshow(M, vmin=vmin, vmax=vmax)
    plt.xticks([])
    plt.yticks([])
    cb = plt.colorbar()

    if save:
        plt.tight_layout()
        plt.savefig(picturename, dpi=dpi)
    
    cb.remove()

    

def plot_surface(M, picturename, zmin, zmax, save, dpi):
    
    m, n = M.shape

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    # Make data
    X, Y = np.meshgrid(np.arange(m), np.arange(n))
    Z = M

    # Plot the surface
    surf = ax.plot_surface(X, Y, Z, cmap='viridis',
                           linewidth=0)

    if zmax:
        ax.set_zlim(zmin, zmax)

    # Remove tick labels on x and y
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # ax.view_init(30, -60)

    # Add a color bar which maps values to colors
    fig.colorbar(surf, shrink=0.5, aspect=5)

    if save:
        plt.tight_layout()
        plt.savefig(picturename, dpi=dpi)
    # plt.show()
    


def make_gif(picture_names, filename, kind, gif_type):
    
    gifname = "Gifs/" + filename + "-" + gif_type + "-" + kind + ".gif"
    
    with imageio.get_writer(gifname, mode='I') as writer:
        for picturename in picture_names:
            image = imageio.imread(picturename)
            writer.append_data(image)
            
    # Remove files
    for picturename in picture_names:
        os.remove(picturename)



def create_all_gifs(X, filename, kind, every=2_000, window=4, max_value=1000, N_max=None):
    # imshow
    imshow_names = movie2png(X, filename, kind, every=every, max_value=max_value, movie_type='imshow', N_max=N_max)
    make_gif(imshow_names, filename, kind, 'imshow')
    
    # surface
    surface_names = movie2png(X, filename, kind, every=every, max_value=max_value, movie_type='surface', N_max=N_max)
    make_gif(surface_names, filename, kind, 'surface')
    
    # catscan
    catscan_names = catscan2png(X[-1], filename, kind, window=window)
    make_gif(catscan_names, filename, kind, 'catscan')

