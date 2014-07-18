from .core import Image
from .exceptions import FileNotFoundException
from os.path import exists


def image_read(file_path):
    if not exists(file_path):
        raise FileNotFoundException(file_path + ' does not exist!')
    return Image(file_path)
