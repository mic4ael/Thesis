from nose.tools import raises
from imagepy import image_read
from imagepy.exceptions import FileNotFoundException
from imagepy.utils import generate_copy_filename


def create_image_object_test():
    file_name = 'images/tree.jpg'
    image = image_read(file_name)
    assert(image is not None)


@raises(FileNotFoundException)
def create_image_object_exception_test():
    file_name = 'wrong_filename'
    image = image_read(file_name)


def decrease_size_test():
    file_name = 'images/sunflower.jpg'
    image = image_read(file_name)
    image.resize(size=(100, 100), new_file_name='images/sunflower_decreased.jpg')


def increase_size_test():
    file_name = 'images/sunflower.jpg'
    image = image_read(file_name)
    image.resize(size=(1000, 1000), new_file_name='images/sunflower_increased.jpg')


def file_name_copy_test():
    file_name = 'test.jpg'
    result = generate_copy_filename(file_name)
    assert(result == 'test_copy.jpg')