import numpy as np
import math

from .exceptions import WrongArgumentType


def _get_ratios(src_size_tuple, dst_size_tuple):
    src_width, src_height = src_size_tuple
    dst_width, dst_height = dst_size_tuple
    return dst_width / src_width, dst_height / src_height


def nearest_neighbours(image, size):
    if not isinstance(size, (tuple,)):
        raise WrongArgumentType("Type must be tuple")

    x_ratio, y_ratio = _get_ratios(image.shape[:2], size)
    result = np.zeros(size[:2] + (3,), dtype=image.dtype)
    for w in range(size[0]):
        for h in range(size[1]):
            px = math.floor(h * x_ratio)
            py = math.floor(w * y_ratio)
            result[w][h] = image[w][px + py]

    return result