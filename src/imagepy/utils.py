from os.path import splitext
import numpy as np
import math

from .exceptions import WrongArgumentType


def generate_copy_filename(file_name):
    name, extension = splitext(file_name)
    new_file_name_template = '{main_name}_copy{extension}'
    return new_file_name_template.format(
        main_name=name,
        extension=extension
    )


def rotate_image(image, degrees):
    pass


def _get_ratios(src_size_tuple, dst_size_tuple):
    src_width, src_height = src_size_tuple
    dst_width, dst_height = dst_size_tuple
    return src_width / dst_width, src_height / dst_height


def nearest_neighbours_scale(image, dst_size):
    if not isinstance(dst_size, (tuple,)):
        raise WrongArgumentType("Size must be tuple")

    x_ratio, y_ratio = _get_ratios(image.shape[:2], dst_size)
    dst_width, dst_height = dst_size
    result = np.zeros((dst_width, dst_height, 3), dtype=image.dtype)
    for w in range(dst_width):
        for h in range(dst_height):
            px = math.floor(w * x_ratio)
            py = math.floor(h * y_ratio)
            result[w][h] = image[px][py]

    return result