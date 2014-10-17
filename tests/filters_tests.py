__author__ = 'mic4ael'

from imagepy import image_read_from_file


def median_filter_test():
    file = 'images/lena.jpg'
    im = image_read_from_file(file)
    im.median_filter()
    im.save('images/m_lena_filtered_median.jpg')