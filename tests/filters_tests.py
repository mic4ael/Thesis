__author__ = 'mic4ael'

from imagepy import image_read_from_file
from imagepy.filters import GaussianFilter, AverageFilter


def median_filter_test():
    file = 'images/lena.jpg'
    im = image_read_from_file(file)
    im.apply_filter(AverageFilter)
    im.save('images/m_lena_filtered_average.jpg')


def gaussian_filter_test():
    file = 'images/lena.jpg'
    im = image_read_from_file(file)
    im.apply_filter(GaussianFilter)
    im.save('images/m_lena_filtered_gaussian.jpg')