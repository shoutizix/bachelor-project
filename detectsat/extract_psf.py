import astropy.io.fits as fits
import utils.prologue as prologue

def main(args):
    x_star,y_star = 3274,7977
    radius = 10
    data = fits.open(args.i)[0].data
    star = data[y_star-radius:y_star+radius, x_star-radius:x_star+radius]

if __name__ == '__main__':
    main(prologue.get_args())