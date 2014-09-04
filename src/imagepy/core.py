from scipy import ndimage
from scipy.misc import imsave

from .utils import nearest_neighbours


class Image(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self._image_arr = ndimage.imread(file_path)

    @property
    def size(self):
        return self._image_arr.shape[:2]

    def resize(self, size, save=False):
        self._image_arr = nearest_neighbours(self._image_arr, size)
        if save:
            imsave(self.file_path, self._image_arr)

    def save(self, save_as_new=False):
        pass