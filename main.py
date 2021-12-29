import pygame as pg

from field import Field
from utils import colors
from shapes import Shape


def main():
    pg.init()

    cell_size = 30
    offset = 100
    size = Field.WIDTH * cell_size + 2 * offset, \
           Field.HEIGHT * cell_size + offset

    offset_x, offset_y = offset, cell_size

    screen = pg.display.set_mode(size)
    pg.display.set_caption('Tetris')

    field = Field(cell_size, offset_x, offset_y)

    timer = pg.time.Clock()
    FPS = 60

    ticks = 0
    speed = 30

    # background_image = pg.image.load()

    running = True
    shape = Shape(field)
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                key = event.key

                if key == pg.K_d or key == pg.K_RIGHT:
                    shape.move_right()
                if key == pg.K_a or key == pg.K_LEFT:
                    shape.move_left()
                if key == pg.K_s or key == pg.K_DOWN:
                    shape.fall()
                if key == pg.K_SPACE:
                    shape.drop()

        screen.fill(colors.get('black'))
        field.render(screen)

        if ticks >= speed:
            shape.fall()
            ticks = 0

        timer.tick(FPS)
        ticks += 1

        pg.display.flip()

    pg.quit()


if __name__ == '__main__':
    main()
