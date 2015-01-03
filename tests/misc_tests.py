from imagepy import image_read_from_file, image_read_from_array, Image
from imagepy.exceptions import FileNotFoundException, WrongArgumentType
from imagepy.utils import generate_copy_filename, median

from nose.tools import raises, assert_raises

from scipy import ndarray

import numpy as np


def file_name_copy_test():
    file_name = 'test.jpg'
    result = generate_copy_filename(file_name)
    assert(result == 'test_copy.jpg')


def create_image_object_from_file_test():
    file_name = 'images/lena.jpg'
    image = image_read_from_file(file_name)
    assert(image is not None)


def create_image_object_from_array_test():
    img = ndarray((10, 10, 3))
    img = image_read_from_array(img)
    assert(img is not None)


@raises(WrongArgumentType)
def create_image_object_from_array_with_exception_test():
    img = ndarray((10, 10, 2))
    image_read_from_array(img)


@raises(WrongArgumentType)
def create_image_from_array_with_exception_test():
    img = ndarray((10, 10))
    image_read_from_array(img)


@raises(FileNotFoundException)
def create_image_object_exception_test():
    file_name = 'wrong_filename'
    image_read_from_file(file_name)


def image_size_test():
    file_name = 'images/sunflower.tiff'
    result = image_read_from_file(file_name)
    assert(result.size == (300, 300))
    assert(result.width == 300)
    assert(result.height == 300)
    image = image_read_from_array(np.zeros((101, 102, 3), dtype=ndarray))
    assert(image.size == (102, 101))
    assert(image.width == 102)
    assert(image.height == 101)


def image_new_test():
    f_args = [(12, 12), (1, 2), (3, 1)]
    for arg in f_args:
        img = Image.new(arg)
        assert(img is not None)
        assert(img.size == arg)


def image_new_with_exception_test():
    f_args = [(21, -15), (12, 0), (0, 0), (-1, -1), (-1, 10), (1, 2, 3)]
    for arg in f_args:
        with assert_raises(WrongArgumentType):
            Image.new(arg)


def median_test():
    data = {
        2: [1, 3, 4, 2, 1],
        3: [3, 2, 3, 4, 5],
        4: [2, 2, 4, 4, 4, 6],
        1: [1],
        5: [5, 6]
    }

    for key, value in data.items():
        assert(key == median(value))