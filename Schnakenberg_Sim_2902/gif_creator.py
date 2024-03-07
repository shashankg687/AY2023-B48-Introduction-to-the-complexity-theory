import glob
import os
from PIL import Image

def create_gif(file_path, delete_images = True):
    """Generates a gif from a series of images in the same directory

    Images must be ordered in directory - ie numercially within the filename. 
    N.B Ensure there are sufficient leading zeroes here - otherwise image2.png 
    will order after image10.png (whereas image02.png does not).
    
    Params:
    file_path [string] - Specifies the location and file name of images to use
                         Should be in the format "Folder/image" where files are
                         named 'image_01.png' etc
    delete_images [boolean] - Defines whether to delete images (default: True)
    """

    fp_in = file_path + "_*.png"
    fp_out =  file_path + ".gif"

    img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
    img.save(fp=fp_out, format='GIF', append_images=imgs,
            save_all=True, duration=200, loop=0)

    if delete_images:
        location = "/".join(file_path.split("/")[:-1]) + '/'
        for file in os.listdir(location):
            if file.endswith('.png'):
                try:
                    os.remove(location + file) 
                except FileNotFoundError:
                    print("Can't find file: " + str(file))
