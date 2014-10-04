from scipy import ndimage
from scipy.misc import imsave

from .utils import nearest_neighbours_scale, rotate_image, get_image_size

from imagepy.exceptions import WrongArgumentType


class Image(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self._image_arr = ndimage.imread(file_path)
        # ndimage.shape returns tuple where first element is height, then width
        self.width, self.height = get_image_size(self._image_arr)

    def resize(self, size):
        self._image_arr = nearest_neighbours_scale(self._image_arr, size)
        self.width, self.height = size

    def rotate(self, angle):
        self._image_arr = rotate_image(self._image_arr, angle)

    def thumbnail(self, size):
        if (isinstance(size, (tuple, list)) and len(size) != 2) \
                or (not isinstance(size, (tuple, list))):
            raise WrongArgumentType('Argument must be iterable and its size must be equal 2')
        width, height = size
        if width < self.width and height < self.width:
            self.width, self.height = size
            self._image_arr = nearest_neighbours_scale(self._image_arr, size)

    def crop(self, size_to_crop):
        # TODO
        pass

    def save(self, file_path=None):
        file_path_to_save = file_path or self.file_path
        imsave(file_path_to_save, self._image_arr)

    @classmethod
    def from_array(cls, image_arr):
        pass

    @classmethod
    def new(cls, size):
        pass

    @classmethod
    def copy(cls, image):
        pass

    @property
    def size(self):
        return self.width, self.height