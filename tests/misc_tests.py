from imagepy import image_read_from_file, image_read_from_array, Image
from imagepy.exceptions import FileNotFoundException, WrongArgumentType
from imagepy.utils import generate_copy_filename

from nose.tools import raises, assert_raises, assert_true

from scipy import ndarray

def file_name_copy_test():
    file_name = 'test.jpg'
    result = generate_copy_filename(file_name)
    assert(result == 'test_copy.jpg')


def create_image_object_from_file_test():
    file_name = 'images/tree.jpg'
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
    file_name = 'images/sunflower.jpg'
    result = image_read_from_file(file_name)
    assert(result.size == (768, 1024))
    assert(result.width == 768)
    assert(result.height == 1024)


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