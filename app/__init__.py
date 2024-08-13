import pygame
from config import Config


def create_app():
    pygame.init()
    conf = Config()

    # game window
    screen = pygame.display.set_mode((conf.SCREEN_WIDTH, conf.SCREEN_HEIGHT))
    pygame.display.set_caption(conf.APP_NAME)

    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()
