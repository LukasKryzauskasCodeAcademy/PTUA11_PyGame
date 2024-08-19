import pygame
from config import Config
from .Fighter import Fighter

conf = Config()


class CreateApp:
    pygame.init()
    # Parameters
    clock = pygame.time.Clock()
    fps = 60
    bottom_panel = conf.BOTTOM_PANEL
    screen_width = conf.SCREEN_WIDTH
    screen_height = conf.SCREEN_HEIGHT + bottom_panel

    # Game window
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(conf.APP_NAME)

    # Load images TODO move image loading to a separate class
    # Background image
    background_img = pygame.image.load('app/img/Background/background.png').convert_alpha()
    # Panel image
    panel_img = pygame.image.load('app/img/Icons/panel.png').convert_alpha()

    # Function for drawing background
    def draw_bg(self):
        # blit() loads an image on specified window
        self.screen.blit(self.background_img, (0, 0))

    # Function for drawing panel
    def draw_panel(self):
        self.screen.blit(self.panel_img, (0, self.screen_height - self.bottom_panel))

    knight = Fighter(200, 260, 'Knight', 30, 10, 3)
    bandit1 = Fighter(550, 270, 'Bandit', 20, 6, 1)
    bandit2 = Fighter(700, 270, 'Bandit', 20, 6, 1)

    bandit_list = [bandit1, bandit2]

    # Function for game loop
    def start(self):
        run = True
        while run:

            self.clock.tick(self.fps)
            # Draw background
            self.draw_bg()
            # Draw panel
            self.draw_panel()
            # Draw Fighters
            self.knight.draw(self.screen)
            for bandit in self.bandit_list:
                bandit.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            pygame.display.update()

        pygame.quit()
