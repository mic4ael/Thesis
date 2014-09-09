from imagepy import image_read


def decrease_size_test():
    file_name = 'images/sunflower.jpg'
    image = image_read(file_name)
    image.resize(size=(200, 100))
    image.save('images/sunflower_decreased.jpg')
    assert(image.size == (200, 100))


def increase_size_test():
    file_name = 'images/sunflower.jpg'
    image = image_read(file_name)
    image.resize(size=(1000, 1200))
    image.save('images/sunflower_increased.jpg')
    assert(image.size == (1000, 1200))


def image_rotate_test():
    file_name = 'images/sunflower.jpg'
    image = image_read(file_name)
    image.rotate(180)
    image.save('images/sunflower_rotated.jpg')