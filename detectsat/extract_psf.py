import astropy.io.fits as fits
import utils.prologue as prologue
from scipy import ndimage
from matplotlib import pyplot as plt
import numpy as np
from utils.mosaic import *
import imageio as imgio

def main(args):
    #x_star,y_star = 3274,7977
    #radius = 10
    x_star,y_star = 3069,7821
    radius = 15
    #x_star,y_star = 2585,7765
    #radius = 5
    data = fits.open(args.i)[0].data

    scaled_data = scale_image(data[::-1].copy())
    star = scaled_data[y_star-radius:y_star+radius, x_star-radius:x_star+radius]
    data_convolved = ndimage.convolve(scaled_data, star, mode='constant', cval=0.0)
    imgio.imwrite('convolved.png', data_convolved)

if __name__ == '__main__':
    main(prologue.get_args())