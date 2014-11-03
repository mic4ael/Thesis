from imagepy import image_read_from_file, image_read_from_array
from imagepy.exceptions import WrongArgumentType

from nose.tools import raises


def decrease_size_test():
    file_name = 'images/sunflower.jpg'
    image = image_read_from_file(file_name)
    image.resize(size=(200, 100))
    image.save('images/m_sunflower_decreased.jpg')
    assert(image.size == (200, 100))


def increase_size_test():
    file_name = 'images/sunflower.jpg'
    image = image_read_from_file(file_name)
    image.resize(size=(1000, 1200))
    image.save('images/m_sunflower_increased.jpg')
    assert(image.size == (1000, 1200))


def image_rotate_test():
    angles = [-180, -90, -45, 0, 45, 90, 180, 360]
    for angle in angles:
        file_name = 'images/sunflower.jpg'
        image = image_read_from_file(file_name)
        image.rotate(angle)
        image.save('images/m_sunflower_rotated_{angle}.jpg'.format(angle=angle))


def thumbnail_test():
    file_name = 'images/sunflower.jpg'
    image = image_read_from_file(file_name)
    image.thumbnail((120, 100))
    image.save('images/m_sunflower_thumbnail.jpg')

@raises(WrongArgumentType)
def thumbnail_wrong_argument_int_test():
    file_name = 'images/sunflower.jpg'
    image = image_read_from_file(file_name)
    image.thumbnail(5)

@raises(WrongArgumentType)
def thumbnail_wrong_argument_too_short_test():
    file_name = 'images/sunflower.jpg'
    image = image_read_from_file(file_name)
    image.thumbnail((1,))

@raises(WrongArgumentType)
def thumbnail_wrong_argument_too_long_test():
    file_name = 'images/sunflower.jpg'
    image = image_read_from_file(file_name)
    image.thumbnail((1, 2, 3))


def vertical_reflection_test():
    file_name = 'images/lena.jpg'
    image = image_read_from_file(file_name)
    image.vertical_reflection()
    image.save('images/m_lena_vertical_reflection.jpg')


def horizontal_reflection_test():
    file_name = 'images/lena.jpg'
    image = image_read_from_file(file_name)
    image.horizontal_reflection()
    image.save('images/m_lena_horizontal_reflection.jpg')


def rgb_split_test():
    file_name = 'images/lena.jpg'
    image = image_read_from_file(file_name)
    r, g, b = image.rgb_channels
    image_read_from_array(r).save('images/m_lena_r.jpg')
    image_read_from_array(g).save('images/m_lena_g.jpg')
    image_read_from_array(b).save('images/m_lena_b.jpg')