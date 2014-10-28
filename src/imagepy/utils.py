import numpy as np
import math

from scipy import ndarray

from .exceptions import WrongArgumentType


def get_image_size(image):
    return image.shape[1::-1]


def generate_copy_filename(file_name):
    from os.path import splitext
    name, extension = splitext(file_name)
    new_file_name_template = '{main_name}_copy{extension}'
    return new_file_name_template.format(
        main_name=name,
        extension=extension
    )


def translate_image(image):
    pass


def rotate_image(image, angle):
    def validate_size(val, max_value):
        if val < 0:
            return 0
        if val >= max_value:
            return max_value - 1
        return val

    if angle == 0 or angle == 360 or angle == -360:
        return image
    angle = math.radians(angle)
    width, height = get_image_size(image)
    cent_x, cent_y = width // 2, height // 2
    rotated_image = np.zeros((width, height, 3), dtype=image.dtype)
    for y in range(height):
        for x in range(width):
            pixel = image[y][x]
            dest_x = validate_size((x - cent_x) * math.cos(angle) - (y - cent_y) * math.sin(angle) + cent_y, height)
            dest_y = validate_size((x - cent_x) * math.sin(angle) + (y - cent_y) * math.cos(angle) + cent_x, width)
            rotated_image[dest_y][dest_x] = pixel
    return rotated_image


def _get_ratios(src_size_tuple, dst_size_tuple):
    src_width, src_height = src_size_tuple
    dst_width, dst_height = dst_size_tuple
    return src_width / dst_width, src_height / dst_height


def nearest_neighbours_scale(image, dst_size):
    if not isinstance(dst_size, (tuple,)):
        raise WrongArgumentType("Size must be tuple")

    x_ratio, y_ratio = _get_ratios(get_image_size(image), dst_size)
    dst_width, dst_height = dst_size
    result = np.zeros((dst_height, dst_width, 3), dtype=image.dtype)
    for y in range(dst_height):
        for x in range(dst_width):
            px = math.floor(x * x_ratio)
            py = math.floor(y * y_ratio)
            result[y][x] = image[py][px]

    return result


def check_is_image(image):
    return isinstance(image, ndarray) and len(image.shape) == 3\
        and image.shape[2] == 3


def median(arg):
    if isinstance(arg, (list, set)):
        sorted_arg = sorted(arg)
        arg_len = len(sorted_arg)
        if arg_len % 2 == 0:
            return (sorted_arg[arg_len // 2] + sorted_arg[(arg_len // 2) + 1]) / 2
        else:
            return sorted_arg[arg_len // 2]