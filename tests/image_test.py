from nose.tools import raises
from imagepy import image_read
from imagepy.exceptions import FileNotFoundException

def create_image_object_test():
    file_name = 'lake.jpeg'
    image = image_read(file_name)
    assert(image is not None)


@raises(FileNotFoundException)
def create_image_object_exception_test():
    file_name = 'wrong_filename'
    image = image_read(file_name)


def resize_test():
    file_name = 'sky.jpeg'
    image = image_read(file_name)
    image.resize(size=(500, 500), save=True)