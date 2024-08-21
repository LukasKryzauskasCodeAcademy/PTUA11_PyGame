import pygame
from config import Config
from .Fighter import Fighter, HealthBar
from .Drawing import Drawer, screen, screen_width, bottom_panel, screen_height

conf = Config()
pygame.init()

# Parameters
fps = conf.FPS
# Define fonts
font = pygame.font.SysFont('Times New Roman', 26)


class CreateApp:
    # Parameters
    clock = pygame.time.Clock()

    pygame.display.set_caption(conf.APP_NAME)
    drawer = Drawer()

    # Create each fighter object
    knight = Fighter(200, 260, 'Knight', 30, 10, 3)
    bandit1 = Fighter(550, 270, 'Bandit', 20, 6, 1)
    bandit2 = Fighter(700, 270, 'Bandit', 20, 6, 1)
    bandit_list = [bandit1, bandit2]

    # Create each fighters healthBar
    knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
    bandit1_health_bar = HealthBar(550, screen_height - bottom_panel + 40, bandit1.hp, bandit1.max_hp)
    bandit2_health_bar = HealthBar(550, screen_height - bottom_panel + 100, bandit2.hp, bandit2.max_hp)

    # Define game variables
    current_fighter = 1  # 1- player
    total_fighters = len(bandit_list) + current_fighter
    action_cooldown = 0
    action_wait_time = 90

    # Function for game loop
    def start(self):
        run = True
        while run:

            self.clock.tick(fps)
            # Draw background
            self.drawer.draw_bg()
            # Draw panel
            self.drawer.draw_panel(self.knight, self.bandit_list)
            self.knight_health_bar.draw(self.knight.hp, screen)
            self.bandit1_health_bar.draw(self.bandit1.hp, screen)
            self.bandit2_health_bar.draw(self.bandit2.hp, screen)

            # Draw Fighters
            self.knight.update()
            self.knight.draw(screen)
            for bandit in self.bandit_list:
                bandit.update()
                bandit.draw(screen)

            # Player action
            if self.knight.alive:
                if self.current_fighter == 1:
                    self.action_cooldown += 1
                    if self.action_cooldown >= self.action_wait_time:
                        # Look for player action
                        # Attack
                        self.knight.attack(self.bandit1)
                        self.current_fighter += 1
                        self.action_cooldown = 0

            # Enemy action
            for count, bandit in enumerate(self.bandit_list):
                if self.current_fighter == 2 + count:
                    if bandit.alive:
                        self.action_cooldown += 1
                        if self.action_cooldown >= self.action_wait_time:
                            # Attack
                            bandit.attack(self.knight)
                            self.current_fighter += 1
                            self.action_cooldown = 0
                    else:
                        self.current_fighter += 1

            # If all fighter had a turn
            if self.current_fighter > self.total_fighters:
                self.current_fighter = 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            pygame.display.update()

        pygame.quit()
