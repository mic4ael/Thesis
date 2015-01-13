from imagepy import image_read_from_file, image_read_from_array
from imagepy.exceptions import WrongArgumentType

from nose.tools import raises

from scipy import ndarray

import numpy as np


def decrease_size_test():
    file_name = 'images/sunflower.tiff'
    image = image_read_from_file(file_name)
    image.resize(size=(200, 100))
    image.save('images/m_sunflower_decreased.tiff')
    assert(image.size == (200, 100))
    image = image_read_from_array(np.zeros((100, 100, 3), dtype=ndarray))
    image.resize(size=(50, 90))
    assert(image.size == (50, 90))


def increase_size_test():
    file_name = 'images/sunflower.tiff'
    image = image_read_from_file(file_name)
    image.resize(size=(500, 700))
    image.save('images/m_sunflower_increased.tiff')
    assert(image.size == (500, 700))
    image = image_read_from_array(np.zeros((100, 100, 3), dtype=ndarray))
    image.resize(size=(250, 350))
    assert(image.size == (250, 350))


def image_rotate_test():
    angles = [-180, -90, -45, 0, 45, 90, 180, 360]
    for angle in angles:
        file_name = 'images/sunflower.tiff'
        image = image_read_from_file(file_name)
        image.rotate(angle)
        image.save('images/m_sunflower_rotated_{angle}.tiff'.format(angle=angle))


def thumbnail_test():
    file_name = 'images/sunflower.tiff'
    image = image_read_from_file(file_name)
    image.thumbnail((50, 50))
    image.save('images/m_sunflower_thumbnail.tiff')
    assert(image.size == (50, 50))


@raises(WrongArgumentType)
def thumbnail_wrong_argument_int_test():
    file_name = 'images/sunflower.tiff'
    image = image_read_from_file(file_name)
    image.thumbnail(5)


@raises(WrongArgumentType)
def thumbnail_wrong_argument_too_short_test():
    file_name = 'images/sunflower.tiff'
    image = image_read_from_file(file_name)
    image.thumbnail((1,))


@raises(WrongArgumentType)
def thumbnail_wrong_argument_too_long_test():
    file_name = 'images/sunflower.tiff'
    image = image_read_from_file(file_name)
    image.thumbnail((1, 2, 3))


def vertical_reflection_test():
    file_name = 'images/lena.jpg'
    image = image_read_from_file(file_name)
    image.vertical_reflection()
    image.save('images/m_lena_vertical_reflection.jpg')
    image = image_read_from_array(np.ones((1, 3, 3), dtype=ndarray))
    image.pixels[0][0] = [1, 2, 3]
    image.vertical_reflection()
    assert(image.pixels.tolist() == [[[1, 1, 1], [1, 1, 1], [1, 2, 3]]])


def horizontal_reflection_test():
    file_name = 'images/lena.jpg'
    image = image_read_from_file(file_name)
    image.horizontal_reflection()
    image.save('images/m_lena_horizontal_reflection.jpg')
    image = image_read_from_array(np.ones((2, 3, 3), dtype=ndarray))
    image.pixels[0][:] = [[1, 2, 3]]
    image.horizontal_reflection()
    assert(image.pixels.tolist() == [[[1, 1, 1], [1, 1, 1], [1, 1, 1]], [[1, 2, 3], [1, 2, 3], [1, 2, 3]]])


def rgb_split_test():
    file_name = 'images/lena.jpg'
    image = image_read_from_file(file_name)
    r, g, b = image.rgb_channels
    image_read_from_array(r).save('images/m_lena_r.jpg')
    image_read_from_array(g).save('images/m_lena_g.jpg')
    image_read_from_array(b).save('images/m_lena_b.jpg')
    image = image_read_from_array(np.zeros((1, 2, 3), dtype=ndarray))
    image.pixels[0][:] = [[3, 4, 2], [5, 6, 7]]
    r, g, b = image.rgb_channels
    assert(r.tolist() == [[[3, 0, 0], [5, 0, 0]]])
    assert(g.tolist() == [[[0, 4, 0], [0, 6, 0]]])
    assert(b.tolist() == [[[0, 0, 2], [0, 0, 7]]])


def invert_image_test():
    file_name = 'images/lena.jpg'
    image = image_read_from_file(file_name)
    image.invert()
    image.save('images/m_lena_inverted.jpg')
    image = image_read_from_array(np.ones((1, 2, 3), dtype=ndarray))
    image.pixels[0][:] = [[200, 100, 123], [0, 1, 4]]
    image.invert()
    assert(image.pixels.tolist() == [[[55, 155, 132], [255, 254, 251]]])


def gray_scale_test():
    file_name = 'images/lena.jpg'
    image = image_read_from_file(file_name)
    image.gray_scale()
    image.save('images/m_lena_gray_scale.jpg')
    image = image_read_from_array(np.ones((1, 2, 3), dtype=ndarray))
    image.pixels[0][:] = [[11, 20, 30], [5, 4, 3]]
    image.gray_scale()
    assert(image.pixels.tolist() == [[[20, 20, 20], [4, 4, 4]]])


def point_operation_test():
    from math import log10
    file_name = 'images/lena.jpg'
    image = image_read_from_file(file_name)
    image.point_operation(lambda x: 145 * log10(x + 1))
    image.save('images/m_lena_log_point.jpg')


def threshold_test():
    file_name = 'images/lena.jpg'
    image = image_read_from_file(file_name)
    image.threshold(114)
    image.save('images/m_lena_threshold.jpg')
    image = image_read_from_array(np.ones((1, 2, 3), dtype=ndarray))
    image.pixels[0][:] = [[200, 200, 200], [30, 0, 45]]
    image.threshold(150)
    assert(image.pixels.tolist() == [[[255, 255, 255], [0, 0, 0]]])


def local_thresholding_test():
    file_name = 'images/adaptive_threshold_test.gif'
    image = image_read_from_file(file_name)
    image.local_adaptive_thresholding(7)
    image.save('images/m_lena_local_threshold.gif')


def otsu_thresholding_test():
    file_name = 'images/otsu_test.jpg'
    image = image_read_from_file(file_name)
    image.otsu_threshold()
    image.save('images/m_otsu_threshold.jpg')


def gaussian_noise_test():
    file_name = 'images/lena.jpg'
    image = image_read_from_file(file_name)
    image.gaussian_noise()
    image.save('images/m_lena_gaussian_noise.jpg')


def salt_and_pepper_noise_test():
    file_name = 'images/lena.jpg'
    image = image_read_from_file(file_name)
    image.salt_and_pepper_noise()
    image.save('images/m_lena_salt_and_pepper_noise.jpg')


def image_histogram_test():
    file_name = 'images/lena.jpg'
    image = image_read_from_file(file_name)
    image.histogram()
    image.save_histogram_to_file('images/m_lena_histogram.png')


def histogram_equalization_test():
    file_name = 'images/unequalized.jpeg'
    image = image_read_from_file(file_name)
    image.gray_scale_histogram()
    image.save_histogram_to_file('images/m_old_histogram_before_equalizing.jpg')
    image.equalize_gray_scale_histogram()
    image.save('images/m_equalized.jpeg')
    image.save_histogram_to_file('images/m_equalized_histogram.jpg')


def histogram_stretching_test():
    file_name = 'images/histogram_stretching.gif'
    image = image_read_from_file(file_name)
    image.gray_scale_histogram()
    image.save_histogram_to_file('images/m_old_histogram_before_stretching.jpg')
    image.stretch_gray_scale_histogram()
    image.save('images/m_histogram_stretching.gif')
    image.save_histogram_to_file('images/m_histogram_stretched.jpg')


def brightness_change_test():
    test_arr = np.zeros((1, 3, 3), dtype=ndarray)
    result_arr = [[[10, 10, 10], [10, 10, 10], [10, 10, 10]]]
    image = image_read_from_array(test_arr)
    image.change_brightness(10)
    assert(image.pixels.tolist() == result_arr)
    image.change_brightness(-20)
    assert(image.pixels.tolist() == test_arr.tolist())
    result_arr = [[[255, 255, 255], [255, 255, 255], [255, 255, 255]]]
    image.change_brightness(300)
    assert(image.pixels.tolist() == result_arr)
    image = image_read_from_file('images/forest.bmp')
    image.change_brightness(60)
    image.save('images/m_forest_illuminated.bmp')
    image.change_brightness(-100)
    image.save('images/m_forest_darkenened.bmp')


def adjusting_contrast_test():
    image = image_read_from_file('images/lena.jpg')
    image.adjust_contrast(-128)
    image.save('images/m_lena_decreased_contrast.jpg')
    image = image_read_from_file('images/lena.jpg')
    image.adjust_contrast(128)
    image.save('images/m_lena_increased_contrast.jpg')


def image_translation_test():
    image = image_read_from_file('images/lena.jpg')
    image.translate(100, 100)
    image.save('images/m_lena_translated.jpg')
    image = image_read_from_file('images/lena.jpg')
    image.translate(-50, 100)
    image.save('images/m_lena_translated_2.jpg')
    image = image_read_from_file('images/lena.jpg')
    image.translate(-50, -50)
    image.save('images/m_lena_translated_3.jpg')