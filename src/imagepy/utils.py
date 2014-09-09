import numpy as np
import math
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


def rotate_image(image, angle):
    width, height = get_image_size(image)
    center_x, center_y = width // 2, height // 2
    rotated_image = np.zeros((height, width, 3), dtype=image.dtype)
    for y in range(height):
        for x in range(width):
            pixel = image[y][x]
            dst_x = (math.cos(angle) * (x - center_x)) + (math.sin(angle) * (y - center_y)) + center_x
            dst_y = (math.sin(angle) * (x - center_x)) + (math.cos(angle) * (y - center_y)) + center_y
            if dst_x < 0:
                dst_x = 0
            if dst_x > width:
                dst_x = width - 1
            if dst_y < 0:
                dst_y = 0
            if dst_y > height:
                dst_y = height - 1
            rotated_image[dst_y][dst_x] = pixel
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