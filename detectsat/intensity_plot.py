import numpy as np
from matplotlib import pyplot as plt
from utils.mosaic import *
from utils.lines import *
from utils.post_processing import *
import utils.prologue as prologue

def plot_intensity(args):
    filename_arg = args.i
    if len(filename_arg) > 0:
        fits_filename = filename_arg
    else:
        fits_filename = 'OMEGA.2020-01-29T04_03_55.177_fullfield_binned.fits'
    pos = args.pos
    filename = 'lines/results_'+pos+'.npy'
    index_image_x = int(filename[-6])
    index_image_y = int(filename[-5])

    raw_img, unscaled_img = get_raw_image(fits_filename)
    crops_addresses = get_blocks_addresses(raw_img)

    row = sorted(crops_addresses.keys())[index_image_x]
    column = crops_addresses[row][index_image_y]
    crop = get_block(raw_img, row, column)
    unscaled_crop = get_block(unscaled_img, row, column)

    lines = np.load(filename, allow_pickle = True)
    h_result = lines
    i = index_image_x
    j = index_image_y

    mm_crop = ((crop - np.min(crop) )/ (np.max(crop) - np.min(crop)) ) * 255
    mm_crop = mm_crop.astype(np.uint8())
    filterSize =(30, 30)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,filterSize)
    tophat_img = cv2.morphologyEx(mm_crop, cv2.MORPH_TOPHAT, kernel)
    (retVal, img_gseuil)=cv2.threshold(tophat_img, 120, 1., cv2.THRESH_BINARY)
    th_crop = np.multiply(crop, img_gseuil)
    lines, rs, ts, bs = get_satellites_blocs(th_crop, h_result, (i,j))
    h,w = th_crop.shape
    new = np.zeros((h,w,3)).astype(int) + mm_crop.reshape(h,w,1).astype(int)
    if len(rs) > 0:
        fig, axes = plt.subplots(len(rs),1,squeeze=False)
        for i, r in enumerate(rs):
            pixels_value_on_line = np.zeros((w,1))
            
            for j in bs[i]:
                bresen_line = build_line(r, ts[i], j, h,w)
                data = new.copy()[bresen_line[:,0], bresen_line[:,1], :]
                for k in range(len(pixels_value_on_line)):
                    pixels_value_on_line[bresen_line[k,1]] += data[k, 0]*0.1140 + data[k, 1]*0.5870 + data[k, 2]*0.2989

                new[bresen_line[:,0], bresen_line[:,1]] = palette[i%5]
            if len(pixels_value_on_line) > 0:
                pixels_value_on_line *= 1/len(bs[i])
                fig.suptitle('Intensity profile of the '+str(len(rs))+' line(s)')
                axes[i,0].plot(pixels_value_on_line[:, 0])
                axes[i,0].legend(['Intensity'])
                """
                plt.figure('Intensity profile'+str(i))
                plt.plot(pixels_value_on_line[:, 0], 'b', pixels_value_on_line[:, 1], 'g', pixels_value_on_line[:, 2], 'r')
                plt.draw()
                plt.legend(['Blue', 'Green', 'Red'])
                plt.ylim((0, 255))
                plt.show()
                """
        plt.savefig('intensity/intensity_'+str(index_image_x)+str(index_image_y)+'.png')
        plt.show()
    else:
        print('There was no satellite on this image !')

if __name__ == '__main__':
    plot_intensity(prologue.get_args())
