import pygame as pg

from field import Field
from utils import colors
from shape import Shape

from screen_utils import game_over_screen


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

    background_image = pg.image.load('./data/assets/bg.jpg')

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
                if key == pg.K_w or key == pg.K_UP:
                    shape.rotate_90deg_clockwise()
                if key == pg.K_SPACE:
                    shape.drop()

        screen.fill(colors.get('black'))
        # screen.blit(background_image, (0, 0))
        field.render(screen)
        field.check_full_rows()

        if shape.collided:

            if shape.game_over():
                screen.fill(colors.get('black'))
                game_over_screen(size, screen, timer, FPS, field)
            shape.normalize_position()
            shape = Shape(field)

        if ticks >= speed:
            shape.fall()
            ticks = 0

        timer.tick(FPS)
        ticks += 1

        pg.display.flip()

    pg.quit()


if __name__ == '__main__':
    main()
