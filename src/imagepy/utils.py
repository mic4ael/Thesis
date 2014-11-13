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


def vertical_reflection(image):
    width, height = get_image_size(image)
    new_image = np.zeros((height, width, 3), dtype=image.dtype)
    for y in range(height):
        for x in range(width):
            pixel = image[y][x]
            new_image[y][width - x - 1] = pixel

    return new_image


def horizontal_reflection(image):
    width, height = get_image_size(image)
    new_image = np.zeros((height, width, 3), dtype=image.dtype)
    for y in range(height):
        for x in range(width):
            pixel = image[y][x]
            new_image[height - y - 1][x] = pixel

    return new_image


def rgb_split(image):
    width, height = get_image_size(image)
    r = np.zeros((height, width, 3), dtype=image.dtype)
    g = np.zeros((height, width, 3), dtype=image.dtype)
    b = np.zeros((height, width, 3), dtype=image.dtype)
    for y in range(height):
        for x in range(width):
            pixel = image[y][x]
            r[y][x] = pixel[0]
            g[y][x] = pixel[1]
            b[y][x] = pixel[2]

    return r, g, b


def invert_image(image):
    width, height = get_image_size(image)
    for y in range(height):
        for x in range(width):
            pixel = image[y][x]
            image[y][x] = 1 - pixel[0], 1 - pixel[1], 1 - pixel[2]


def image_gray_scale(image):
    width, height = get_image_size(image)
    for y in range(height):
        for x in range(width):
            pixel = image[y][x]
            image[y][x] = [sum(pixel) / 3 for _ in range(3)]


def image_thresholding(image, threshold):
    width, height = get_image_size(image)
    for y in range(height):
        for x in range(width):
            pixel = image[y][x]
            new_val = 255 if pixel[0] >= threshold else 0
            image[y][x] = [new_val for _ in range(3)]