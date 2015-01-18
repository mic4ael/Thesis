from .core import Image
from .exceptions import FileNotFoundException
from .filters import *

from os.path import exists


def image_read_from_file(file_path):
    if not exists(file_path):
        raise FileNotFoundException(file_path + ' does not exist!')

    return Image(file_path=file_path)


def image_read_from_array(image_array):
    return Image(file_array=image_array)


__all__ = ['Image', 'image_read_from_array', 'image_read_from_file']
for filter_class in list(filter(lambda x: str(x).endswith('Filter'), dir())):
    __all__.append(filter_class)
