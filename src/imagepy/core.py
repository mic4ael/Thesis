import matplotlib.pyplot as plot
import pylab

from scipy import ndimage, zeros
from scipy.misc import imsave

from .operations import nearest_neighbours_scale, rotate_image, \
    get_image_size, check_is_image, vertical_reflection, \
    horizontal_reflection, rgb_split, invert_image, image_gray_scale,\
    image_thresholding, add_gaussian_noise, salt_and_pepper_noise, \
    image_histogram, equalize_gray_scale_histogram, gray_scale_image_histogram, \
    stretch_gray_scale_histogram, assert_pixel_value, otsu_threshold, translate_image, \
    local_adaptive_thresholding

from .filters import SharpeningFilter, AverageFilter

from .exceptions import WrongArgumentType


class Image(object):
    def __init__(self, file_path=None, file_array=None):
        self._file_path = None
        self._image_arr = None
        self.histogram_data = {}

        if file_path:
            self._file_path = file_path
            self._image_arr = ndimage.imread(file_path, mode='RGB')

        if file_array is not None:
            if check_is_image(file_array):
                self._image_arr = file_array
            else:
                raise WrongArgumentType('File array must be of ndarray type')

        # ndimage.shape returns tuple where first element is height, then width
        if self._image_arr is not None:
            self.width, self.height = get_image_size(self._image_arr)

    def resize(self, size):
        self._image_arr = nearest_neighbours_scale(self._image_arr, size)
        self.width, self.height = get_image_size(self._image_arr)

    def rotate(self, angle):
        self._image_arr = rotate_image(self._image_arr, angle)

    def translate(self, x, y):
        self._image_arr = translate_image(self._image_arr, x, y)

    def thumbnail(self, size):
        if (isinstance(size, (tuple, list)) and len(size) != 2) \
                or (not isinstance(size, (tuple, list))):
            raise WrongArgumentType('Argument must be iterable and its size must be equal 2')
        width, height = size
        if width < self.width and height < self.width:
            self.width, self.height = size
            self._image_arr = nearest_neighbours_scale(self._image_arr, size)

    def apply_filter(self, filter_cls):
        self._image_arr = filter_cls.apply_filter(self._image_arr)

    def save(self, file_path=None):
        imsave(file_path or self._file_path, self._image_arr)

    def horizontal_reflection(self):
        self._image_arr = horizontal_reflection(self._image_arr)

    def vertical_reflection(self):
        self._image_arr = vertical_reflection(self._image_arr)

    def get_pixel_at(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise Exception

        return self._image_arr[y][x]

    def histogram(self):
        self.histogram_data = image_histogram(self._image_arr)
        return self.histogram_data

    def gray_scale_histogram(self):
        self.histogram_data = gray_scale_image_histogram(self._image_arr)
        return self.histogram_data

    def save_histogram_to_file(self, file_name):
        x_axis = list(range(256))
        try:
            r_y = list(self.histogram_data['r'].values())
            g_y = list(self.histogram_data['g'].values())
            b_y = list(self.histogram_data['b'].values())
            plot.stem(x_axis, r_y, linefmt='r', markerfmt=' ')
            plot.stem(x_axis, g_y, linefmt='g', markerfmt=' ')
            plot.stem(x_axis, b_y, linefmt='b', markerfmt=' ')
        except KeyError:
            plot.stem(x_axis, list(self.histogram_data.values()), markerfmt=' ')

        pylab.savefig(file_name)
        pylab.close()

    def invert(self):
        invert_image(self._image_arr)

    def gray_scale(self):
        image_gray_scale(self._image_arr)

    def gaussian_noise(self, mean=0, variance=20):
        self._image_arr = add_gaussian_noise(self._image_arr, mean, variance)

    def salt_and_pepper_noise(self, f_prob, s_prob, min_pixel_value=0, max_pixel_value=255):
        if f_prob + s_prob > 1:
            raise Exception('Too big values for probabilities')

        salt_and_pepper_noise(self._image_arr, f_prob, min_pixel_value, s_prob, max_pixel_value)

    def point_operation(self, func):
        for y in range(self.height):
            for x in range(self.width):
                pixel = self._image_arr[y, x]
                self._image_arr[y, x] = [assert_pixel_value(func(i)) for i in pixel]

    def threshold(self, threshold):
        image_thresholding(self._image_arr, threshold)

    def otsu_threshold(self):
        image_thresholding(self._image_arr, otsu_threshold(self._image_arr))

    def local_adaptive_thresholding(self, block_size):
        local_adaptive_thresholding(self._image_arr, block_size)

    def equalize_gray_scale_histogram(self):
        equalize_gray_scale_histogram(self._image_arr)
        self.histogram_data = gray_scale_image_histogram(self._image_arr)

    def stretch_gray_scale_histogram(self):
        stretch_gray_scale_histogram(self._image_arr)
        self.histogram_data = gray_scale_image_histogram(self._image_arr)

    def change_brightness(self, factor):
        for y in range(self.height):
            for x in range(self.width):
                pixel = self._image_arr[y, x]
                self._image_arr[y][x] = [assert_pixel_value(el + factor) for el in pixel]

    def adjust_contrast(self, contrast):
        contrast_factor = (259 * (259 + contrast)) / (259 * (259 - contrast))
        f = lambda arg: contrast_factor * (arg - 128) + 128
        for y in range(self.height):
            for x in range(self.width):
                pixel = self._image_arr[y][x]
                self._image_arr[y][x] = [assert_pixel_value(f(el)) for el in pixel]

    def sharpen(self):
        self.apply_filter(SharpeningFilter)

    def denoise(self):
        self.apply_filter(AverageFilter)

    @classmethod
    def new(cls, size):
        def check_arguments(f_args):
            if any([True for arg in f_args if arg <= 0]):
                raise WrongArgumentType('One of provided arguments is <= 0!')

        check_arguments(size)
        img = zeros(size[::-1] + (3, ))
        return Image(file_array=img)

    @classmethod
    def copy(cls, image_arr):
        return Image(file_array=image_arr)

    @property
    def size(self):
        return self.width, self.height

    @property
    def rgb_channels(self):
        self.r, self.g, self.b = rgb_split(self._image_arr)
        return self.r, self.g, self.b

    @property
    def pixels(self):
        return self._image_arr


__all__ = ['Image']
