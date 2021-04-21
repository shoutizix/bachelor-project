import astropy.io.fits as fits
import utils.prologue as prologue
from scipy import ndimage
from scipy.optimize import curve_fit
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
    width = 1900
    value = 1
    ampl, period, phase_shift, vertical_shift = 0.5, 0.01, 0, 0.5

    blank_image = np.zeros((height,width))
    data = fits.open(args.i)[0].data
    star = data[y_star-radius:y_star+radius, x_star-radius:x_star+radius]
    height_line = 2*radius
    line = np.zeros((height_line, width))

    for i in range(height_line):
        for j in range(width):
            if(i == round(height_line/2)):
                line[i,j] = sinus(j, ampl, period, phase_shift, vertical_shift)
                #line[i,j] = value*sinus(j, ampl, period, phase_shift, vertical_shift)

    line_convolved = ndimage.convolve(line, star)
    findIntensityAlongTheLine(line, height_line, width, 0, 0)
    #showGraph(np.transpose(line_convolved))
    #Put the same value in the last row as in the first one
    line_convolved[-1,:] = line_convolved[0,:]
    line_convolved[:,:] = line_convolved[:,:]-(51.4*2)
    #createImage('line_convolved_reflect_4r.png', line_convolved)


    #data_with_line = addLineOnData(line_convolved, data, width, height_line)
    #scaled_data = scale_image(data_with_line[::-1].copy())
    #findIntensityAlongTheLine(scaled_data, height_line, width, 100, 100)
    #createImage('try_image_line_new_star_15_04_r.png', scaled_data)


    #createFitsFile(args.i, scaled_data)
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
    #print(data[min_y:min_y+height_line, min_x:min_x+width_line])
    data[min_y:min_y+height_line, min_x:min_x+width_line] += line[:,:]
    #print('-----------------------')
    #print(data[min_y:min_y+height_line, min_x:min_x+width_line])
    return data

def findIntensityAlongTheLine(data, height_line, width_line, start_line_x, start_line_y):
    intensities = []
    for i in range(width_line):
        intensity_for_this_x = 0
        for j in range(height_line):
            intensity_for_this_x += data[start_line_y+j,start_line_x+i]
        intensities.append(intensity_for_this_x)
        #intensities.append(intensity_for_this_x/height_line)



    fig, ax = plt.subplots(1, 2)
    ax = ax.flatten()
    ax[0].plot(intensities)
    ax[0].set_title("Original signal")

    intensities_fft = np.fft.fft(intensities)
    intensities_fft = intensities_fft[:round(width_line/2)]
    intensities_fft = np.abs(intensities_fft)
    intensities_fft = intensities_fft/max(intensities_fft)
    freq_x_axis = np.linspace(0, width_line/2, len(intensities_fft))
    ax[1].plot(freq_x_axis, intensities_fft, "o-")
    ax[1].set_title("Frequency magnitudes")
    ax[1].set_xlabel("Frequency")
    ax[1].set_ylabel("Magnitude")
    plt.grid()
    plt.tight_layout()
    plt.show()

    f_loc = np.argmax(intensities_fft) # Finds the index of the max
    f_val = freq_x_axis[f_loc] # The strongest frequency value
    print(f"The strongest frequency is f = {f_val}")


    x_val = np.arange(width_line)
    showGraph(np.transpose(intensities))
    params, _ = curve_fit(sinus, x_val, intensities)
    print(params)
    
    plt.scatter(x_val, intensities, label='Data')
    plt.plot(x_val, sinus(x_val, params[0], params[1], params[2], params[3]), color='red', label='Fitted function')
    plt.legend(loc='best')
    plt.show()
    
    #intensities_fft = np.fft.fft(intensities)
    #intensities_fft = intensities_fft[:round(width_line/2)]
    #intensities_fft = np.abs(intensities_fft)
    #intensities_fft = intensities_fft/max(intensities_fft)


    

def createFitsFile(name, array):
    hdu = fits.PrimaryHDU(array)
    hdu.writeto(name+'.fits')

    

if __name__ == '__main__':
    main(prologue.get_args())