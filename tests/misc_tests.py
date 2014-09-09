from imagepy import image_read
from imagepy.exceptions import FileNotFoundException
from imagepy.utils import generate_copy_filename

from nose.tools import raises


def file_name_copy_test():
    file_name = 'test.jpg'
    result = generate_copy_filename(file_name)
    assert(result == 'test_copy.jpg')


def create_image_object_test():
    file_name = 'images/tree.jpg'
    image = image_read(file_name)
    assert(image is not None)


@raises(FileNotFoundException)
def create_image_object_exception_test():
    file_name = 'wrong_filename'
    image_read(file_name)


def image_size_test():
    file_name = 'images/sunflower.jpg'
    result = image_read(file_name)
    assert(result.size == (768, 1024))
    assert(result.width == 768)
    assert(result.height == 1024)