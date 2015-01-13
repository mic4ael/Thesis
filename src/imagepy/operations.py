import numpy as np
import math
import random
import operator

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


def translate_image(image, d_x, d_y):
    width, height = get_image_size(image)
    result = np.zeros((height, width, 3), dtype=image.dtype)
    for y in range(height):
        for x in range(width):
            yy = d_y + y
            if yy >= height:
                yy = height - 1
            if yy < 0:
                yy = 0
            xx = d_x + x
            if xx >= width:
                xx = width - 1
            if xx < 0:
                xx = 0

            result[yy, xx] = image[y, x]

    return result


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
            dest_x = validate_size((x - cent_x) * math.cos(angle) - (y - cent_y) * math.sin(angle) + cent_y, height)
            dest_y = validate_size((x - cent_x) * math.sin(angle) + (y - cent_y) * math.cos(angle) + cent_x, width)
            rotated_image[dest_y, dest_x] = image[y, x]

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
            result[y, x] = image[py, px]

    return result


def check_is_image(image):
    return isinstance(image, ndarray) and len(image.shape) == 3\
        and image.shape[2] == 3


def median(arg):
    if isinstance(arg, (list, tuple, set)):
        sorted_arg = sorted(arg)
        arg_len = len(sorted_arg)
        index = (arg_len - 1) // 2
        if index % 2 != 0:
            return (sorted_arg[index] + sorted_arg[index + 1]) / 2
        else:
            return sorted_arg[index]

    raise WrongArgumentType('Argument must be tuple, list or set')


def horizontal_reflection(image):
    width, height = get_image_size(image)
    new_image = np.zeros((height, width, 3), dtype=image.dtype)
    for y in range(height):
        for x in range(width):
            new_image[y, width - x - 1] = image[y, x]

    return new_image


def vertical_reflection(image):
    width, height = get_image_size(image)
    new_image = np.zeros((height, width, 3), dtype=image.dtype)
    for y in range(height):
        for x in range(width):
            new_image[height - y - 1, x] = image[y, x]

    return new_image


def rgb_split(image):
    width, height = get_image_size(image)
    r = np.zeros((height, width, 3), dtype=image.dtype)
    g = np.zeros((height, width, 3), dtype=image.dtype)
    b = np.zeros((height, width, 3), dtype=image.dtype)
    for y in range(height):
        for x in range(width):
            r[y][x][0], g[y][x][1], b[y][x][2] = image[y][x]

    return r, g, b


def invert_image(image):
    width, height = get_image_size(image)
    for y in range(height):
        for x in range(width):
            image[y, x] = list(map(lambda arg: 255 - arg, image[y, x]))


def image_gray_scale(image):
    width, height = get_image_size(image)
    for y in range(height):
        for x in range(width):
            image[y, x] = [sum(image[y, x]) // 3] * 3


def image_thresholding(image, threshold):
    image_gray_scale(image)
    width, height = get_image_size(image)
    for y in range(height):
        for x in range(width):
            pixel = image[y, x]
            new_val = 255 if pixel[0] >= threshold else 0
            image[y, x] = [new_val, new_val, new_val]


def add_gaussian_noise(image, mean, variance):
    noise = np.random.normal(mean, variance, image.shape)
    return image + noise


def salt_and_pepper_noise(image, f_prob, min_p_val, s_prob, max_p_val):
    image_gray_scale(image)
    width, height = get_image_size(image)
    for y in range(height):
        for x in range(width):
            rand_number = random.random()
            if 0 <= rand_number < f_prob:
                image[y, x] = [min_p_val, min_p_val, min_p_val]
            elif f_prob <= rand_number < f_prob + s_prob:
                image[y, x] = [max_p_val, max_p_val, max_p_val]


def image_histogram(image):
    width, height = get_image_size(image)
    ret = {key: {i: 0 for i in range(256)} for key in 'rgb'}
    for y in range(height):
        for x in range(width):
            ret['r'][image[y, x, 0]] += 1
            ret['g'][image[y, x, 1]] += 1
            ret['b'][image[y, x, 2]] += 1

    return ret


def gray_scale_image_histogram(image):
    width, height = get_image_size(image)
    ret = {index: 0 for index in range(256)}
    for y in range(height):
        for x in range(width):
            g_s = sum(image[y, x]) // 3
            ret[g_s] += 1

    return ret


def equalize_gray_scale_histogram(image):
    image_gray_scale(image)
    width, height = get_image_size(image)
    number_of_pixels = width * height
    gray_scale_histogram = gray_scale_image_histogram(image)
    values = {}
    s = 0
    for key, value in gray_scale_histogram.items():
        s += value
        values[key] = {
            'count': value,
            'cdf': s,
            'cdf_scaled': 0
        }

    min_cdf = None
    for key, value in values.items():
        if value['cdf'] != 0 and (min_cdf is None or value['cdf'] < min_cdf):
            min_cdf = value['cdf']

    for key, value in values.items():
        dest_val = round(((value['cdf'] - min_cdf) / (number_of_pixels - min_cdf)) * 255)
        if dest_val > 255:
            dest_val = 255

        value['cdf_scaled'] = dest_val

    for y in range(height):
        for x in range(width):
            image[y, x] = [values[image[y, x, 0]]['cdf_scaled']] * 3


def stretch_gray_scale_histogram(image):
    image_gray_scale(image)
    width, height = get_image_size(image)
    gray_scale_histogram = gray_scale_image_histogram(image)
    sorted_grayscale = list(filter(
        lambda el: el[1] != 0,
        sorted(gray_scale_histogram.items(), key=operator.itemgetter(0)))
    )
    min_intensity, max_intensity = sorted_grayscale[0][0], sorted_grayscale[-1][0]
    if max_intensity == 255:
        max_intensity = 254

    for y in range(height):
        for x in range(width):
            new_val = assert_pixel_value(((image[y, x, 0] - min_intensity) / (max_intensity - min_intensity)) * 255)
            image[y, x] = [new_val, new_val, new_val]


def assert_pixel_value(val):
    if val < 0:
        return 0
    if val > 255:
        return 255

    return val


def otsu_threshold(image):
    width, height = get_image_size(image)
    histogram = gray_scale_image_histogram(image)
    wB, wF, sum, sumB, mB, mF, between, max, result = 0, 0, 0, 0, 0, 0, 0, 0, 0

    for i in range(256):
        sum += i * histogram[i]

    for intensity in range(256):
        wB += histogram[intensity]
        if wB == 0:
            continue

        wF = (width * height) - wB
        if wF == 0:
            break

        sumB += intensity * histogram[intensity]
        mB = sumB / wB
        mF = (sum - sumB) / wF
        between = wB * wF * ((mB - mF) ** 2)
        if between > max:
            max = between
            result = intensity

    return result


def local_adaptive_thresholding(image, block_size):
    width, height = get_image_size(image)
    t = block_size // 2

    for y in range(t, height - t):
        for x in range(t, width - t):
            sub_image = image[np.ix_(list(range(y - t, y + t + 1)), list(range(x - t, x + t + 1)))]
            histogram = gray_scale_image_histogram(sub_image)
            d = list({key: value for key, value in histogram.items() if value != 0}.keys())
            new_pixel_val = 255 if image[y, x, 0] >= median(d) else 0
            image[y, x] = [new_pixel_val, new_pixel_val, new_pixel_val]


_not_in_public_api = ['ndarray', 'math', 'operator', 'np', 'WrongArgumentType', 'random']
__all__ = [str(element) for element in dir() if not element.startswith('_') and element not in _not_in_public_api]
