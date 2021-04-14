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
    #x_star,y_star = 2585,7765
    #radius = 5
    #x_star,y_star = 3069,7821
    #x_star,y_star = 1175,7541
    #x_star,y_star = 1639,7812
    x_star,y_star = 1665,8346
    radius = 15
    height = 2000
    width = 2000
    value = 0.02
    ampl, period, phase_shift, vertical_shift = 0.01, 0.01, 0, 0.5

    blank_image = np.zeros((height,width))
    data = fits.open(args.i)[0].data
    star = data[y_star-radius:y_star+radius, x_star-radius:x_star+radius]
    height_line = 2*radius
    line = np.zeros((height_line, width))

    for i in range(height_line):
        for j in range(width):
            if(i == height_line/2):
                line[i,j] = value*sinus(j, ampl, period, phase_shift, vertical_shift)

    line_convolved = ndimage.convolve(line, star)
    #Put the same value in the last row as in the first one
    line_convolved[-1,:] = line_convolved[0,:]
    line_convolved[:,:] = line_convolved[:,:]-(51.4*2)
    #createImage('line_convolved_reflect_4r.png', line_convolved)
    data_with_line = addLineOnData(line_convolved, data, width, height_line)
    scaled_data = scale_image(data_with_line[::-1].copy())
    createImage('try_image_line_new_star_14_04.png', scaled_data)
    #showGraph(np.transpose(line_convolved))


def sinus(angle, ampl, period, phase_shift, vertical_shift):
    return ampl*np.sin(period*angle+phase_shift)+vertical_shift

def createImage(name, array):
    imgio.imwrite(name, array)

def showGraph(array):
    plt.plot(array)
    plt.show()

def addLineOnData(line, data, width_line, height_line):
    #For the first block of the fits file (bottom left)
    min_x, min_y = 100, 100
    max_x, max_y = 2000, 4000
    print(data[min_y:min_y+height_line, min_x:min_x+width_line])
    data[min_y:min_y+height_line, min_x:min_x+width_line] += line[:,:]
    print('-----------------------')
    print(data[min_y:min_y+height_line, min_x:min_x+width_line])
    return data

    

if __name__ == '__main__':
    main(prologue.get_args())