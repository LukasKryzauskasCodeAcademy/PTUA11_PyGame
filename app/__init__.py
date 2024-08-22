import pygame
pygame.init()
from config import Config
from .Fighter import Fighter, HealthBar
from .Drawing import Drawer, DamageText, green, red, screen, screen_width, bottom_panel, screen_height
from .Button import Button

conf = Config()

# Parameters
fps = conf.FPS

# Group is similar to python list
damage_text_group = pygame.sprite.Group()

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
    attack = False
    potion = False
    potion_effect = 15
    clicked = False

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
            # Create buttons
            potion_button = Button(screen, 100, screen_height - bottom_panel + 70, self.drawer.potion_img, 64, 64)

            # Draw Fighters
            self.knight.update()
            self.knight.draw(screen)
            for bandit in self.bandit_list:
                bandit.update()
                bandit.draw(screen)

            # Draw damage text
            damage_text_group.update()
            damage_text_group.draw(screen)

            # Control player actions
            # Reset action variables
            self.attack = False
            self.potion = False
            target = None
            # Make sure mouse is Visible
            pygame.mouse.set_visible(True)
            # Get mouse position
            pos = pygame.mouse.get_pos()
            for count, bandit in enumerate(self.bandit_list):
                if bandit.rect.collidepoint(pos):
                    # Hide mouse
                    pygame.mouse.set_visible(False)
                    # Show sword in place of mouse cursor
                    screen.blit(self.drawer.sword_img, pos)
                    if self.clicked and bandit.alive:
                        self.attack = True
                        target = self.bandit_list[count]

            # Draw buttons
            if potion_button.draw():
                self.potion = True
            self.drawer.draw_text(str(self.knight.potions), red, 150, screen_height - bottom_panel + 70)

            # Player action
            if self.knight.alive:
                if self.current_fighter == 1:
                    self.action_cooldown += 1
                    if self.action_cooldown >= self.action_wait_time:
                        # Look for player action
                        # Attack
                        if self.attack and target is not None:
                            self.knight.attack(target)

                            self.current_fighter += 1
                            self.action_cooldown = 0
                        # Potion
                        if self.potion:
                            if self.knight.potions > 0:
                                # Check if potion would heal beyond max hp
                                if self.knight.max_hp - self.knight.hp > self.potion_effect:
                                    heal_amount = self.potion_effect
                                else:
                                    heal_amount = self.knight.max_hp - self.knight.hp
                                self.knight.hp += heal_amount
                                self.knight.potions -= 1
                                # Healing text
                                damage_text = DamageText(self.knight.rect.centerx, self.knight.rect.y, str(heal_amount),
                                                         green)
                                damage_text_group.add(damage_text)

                                self.current_fighter += 1
                                self.action_cooldown = 0

            # Enemy action
            for count, bandit in enumerate(self.bandit_list):
                if self.current_fighter == 2 + count:
                    if bandit.alive:
                        self.action_cooldown += 1
                        if self.action_cooldown >= self.action_wait_time:
                            # Check if bandit needs to heal
                            if (bandit.hp / bandit.max_hp) < 0.5 and bandit.potions > 0:
                                # Check if potion would heal beyond max hp
                                if bandit.max_hp - bandit.hp > self.potion_effect:
                                    heal_amount = self.potion_effect
                                else:
                                    heal_amount = bandit.max_hp - bandit.hp
                                bandit.hp += heal_amount
                                bandit.potions -= 1
                                # Healing text
                                damage_text = DamageText(bandit.rect.centerx, bandit.rect.y, str(heal_amount),
                                                         green)
                                damage_text_group.add(damage_text)

                                self.current_fighter += 1
                                self.action_cooldown = 0
                            # Attack
                            else:
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True
                else:
                    self.clicked = False

            pygame.display.update()

        pygame.quit()
