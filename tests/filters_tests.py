__author__ = 'mic4ael'

from imagepy import image_read_from_file
from imagepy.filters import GaussianFilter, AverageFilter,\
    SquareFilter, MinFilter, MaxFilter, MedianFilter, SharpeningFilter

from tests import profile


@profile
def average_filter_test():
    file = 'images/lena.jpg'
    im = image_read_from_file(file)
    im.apply_filter(AverageFilter)
    im.save('images/m_lena_filtered_average.jpg')


@profile
def gaussian_filter_test():
    file = 'images/lena.jpg'
    im = image_read_from_file(file)
    im.apply_filter(GaussianFilter)
    im.save('images/m_lena_filtered_gaussian.jpg')


@profile
def square_filter_test():
    file = 'images/lena.jpg'
    im = image_read_from_file(file)
    im.apply_filter(SquareFilter)
    im.save('images/m_lena_filtered_square.jpg')


@profile
def max_min_filter_test():
    file = 'images/lena.jpg'
    im = image_read_from_file(file)
    im.apply_filter(MinFilter)
    im.save('images/m_lena_filtered_min.jpg')
    im = image_read_from_file(file)
    im.apply_filter(MaxFilter)
    im.save('images/m_lena_filtered_max.jpg')


@profile
def median_filter_test():
    file = 'images/lena.jpg'
    im = image_read_from_file(file)
    im.apply_filter(MedianFilter)
    im.save('images/m_lena_filtered_median.jpg')


@profile
def sharpening_filter_test():
    file = 'images/lena.jpg'
    im = image_read_from_file(file)
    im.sharpen()
    im.save('images/m_lena_filtered_sharpened.jpg')


@profile
def denoising_test():
    file = 'images/noised_image.jpg'
    im = image_read_from_file(file)
    im.denoise()
    im.save('images/m_denoised.jpg')