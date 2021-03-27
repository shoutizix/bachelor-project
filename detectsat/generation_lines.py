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
    height = 300
    width = 1000
    value = 0.01
    x_star,y_star = 3069,7821
    radius = 15
    ampl, period, phase_shift, vertical_shift = 0.5, 0.1, 0, 0.5
    #x_star,y_star = 2585,7765
    #radius = 5
    blank_image = np.zeros((height,width))
    data = fits.open(args.i)[0].data
    
    #scaled_data = scale_image(data[::-1].copy())
    #print(np.shape(scaled_data))
    star = data[y_star-radius:y_star+radius, x_star-radius:x_star+radius]
    #print(star)
    #print(np.shape(star))
    line = np.zeros((2*radius, width))
    for i in range(2*radius):
        for j in range(width):
            # Change this to use a sinusoidal function
            if(i == radius):
                line[i,j] = value*sinus(j, ampl, period, phase_shift, vertical_shift)
    line_convolved = ndimage.convolve(line, star)
    
    plt.plot(np.transpose(line_convolved))
    plt.show()  

def sinus(angle, ampl, period, phase_shift, vertical_shift):
    return ampl*np.sin(period*angle+phase_shift)+vertical_shift

    

if __name__ == '__main__':
    main(prologue.get_args())