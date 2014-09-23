from imagepy import image_read


def decrease_size_test():
    file_name = 'images/sunflower.jpg'
    image = image_read(file_name)
    image.resize(size=(200, 100))
    image.save('images/m_sunflower_decreased.jpg')
    assert(image.size == (200, 100))


def increase_size_test():
    file_name = 'images/sunflower.jpg'
    image = image_read(file_name)
    image.resize(size=(1000, 1200))
    image.save('images/m_sunflower_increased.jpg')
    assert(image.size == (1000, 1200))


def image_rotate_test():
    angles = [-180, -90, -45, 0, 45, 90, 180, 360]
    for angle in angles:
        file_name = 'images/sunflower.jpg'
        image = image_read(file_name)
        image.rotate(angle)
        image.save('images/m_sunflower_rotated_{angle}.jpg'.format(angle=angle))