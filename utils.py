import pygame
import os


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


colors = {
    'black': (0, 0, 0),
    'white': (255, 255, 255),
    'light yellow': (252, 255, 71),
    'cyan': (27, 245, 223),
    'orange': (245, 153, 15),
    'light green': (86, 255, 43),
    'purple': (241, 27, 245),
    'dark green': (8, 117, 37),
    'red': (255, 0, 0)
}
