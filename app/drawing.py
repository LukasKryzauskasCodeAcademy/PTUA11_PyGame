import pygame
from config import Config

conf = Config()

# Game window
bottom_panel = conf.BOTTOM_PANEL
screen_width = conf.SCREEN_WIDTH
screen_height = conf.SCREEN_HEIGHT + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))

# Define fonts
font = pygame.font.SysFont('Times New Roman', 26)

# Function for drawing text
#TODO change the x, y coordinates to be text center not top left corner
def draw_text(text, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


def draw_button_text(text, text_color, x, y, image_rect):
    text = font.render(text, True, text_color)
    text_rect = text.get_rect(center=(image_rect.width / 2 + x, image_rect.height / 2 + y))
    screen.blit(text, text_rect)


class Drawer:
    # Load images
    # Background image
    background_img = pygame.image.load('app/img/Background/background.png').convert_alpha()
    # Panel image
    panel_img = pygame.image.load('app/img/Icons/panel.png').convert_alpha()
    # Cursor image
    sword_img = pygame.image.load('app/img/Icons/sword.png').convert_alpha()
    # Button images
    potion_img = pygame.image.load('app/img/Icons/potion.png').convert_alpha()
    restart_img = pygame.image.load('app/img/Icons/restart.png').convert_alpha()

    button_img = pygame.image.load('app/img/Icons/button.png').convert_alpha()
    # Load Victory and Defeat images
    victory_img = pygame.image.load('app/img/Icons/victory.png').convert_alpha()
    defeat_img = pygame.image.load('app/img/Icons/defeat.png').convert_alpha()
    # Load game logo
    logo_img = pygame.image.load('app/img/Icons/logo.png').convert_alpha()
    logo_img = pygame.transform.scale(logo_img, (logo_img.get_width() *0.4, logo_img.get_height() *0.35))

    # Function for drawing background
    def draw_bg(self):
        # blit() loads an image on specified window, and position
        screen.blit(self.background_img, (0, 0))

    # Function for drawing panel
    def draw_panel(self, knight, bandit_list):
        # Draw panel rectangle
        screen.blit(self.panel_img, (0, screen_height - bottom_panel))
        # Show knight stats
        draw_text(f'{knight.name} HP: {knight.hp}', "red", 100,
                       screen_height - bottom_panel + 10)
        for count, bandit in enumerate(bandit_list):
            # Show name and health for each bandit
            draw_text(f'{bandit.name} HP: {bandit.hp}', "red", 550,
                           (screen_height - bottom_panel + 10) + count * 60)


# Sprite class has an inbuilt draw and update method
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # Move damage text up
        self.rect.y -= 1
        # Delete text after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()
