import pygame
from .drawing import draw_button_text


class Button:
    def __init__(self, surface, x, y, image, size_x, size_y):
        self.image = pygame.transform.scale(image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.surface = surface

    def draw(self, text=None):
        action = False
        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw button
        self.surface.blit(self.image, (self.rect.x, self.rect.y))
        # Draw text on top
        if text:
            draw_button_text(text, "white", self.rect.x, self.rect.y, self.rect)

        return action


class Slider:
    def __init__(self, pos: tuple, size: tuple, initial_val: float, min: int, max: int):
        self.pos = pos
        self.size = size

        self.slider_left_pos = self.pos[0] - (size[0] // 2)
        self.slider_right_pos = self.pos[0] + (size[0] // 2)
        self.slider_top_pos = self.pos[1] - (size[1] // 2)

        self.min = min
        self.max = max
        # Percentage position
        self.initial_val = (self.slider_right_pos - self.slider_left_pos) * initial_val

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + self.initial_val - 5, self.slider_top_pos, 10,
                                       self.size[1])

    def move_slider(self, mouse_pos):
        self.button_rect.centerx = mouse_pos[0]

    def render(self, surface):
        pygame.draw.rect(surface, "darkgray", self.container_rect)
        pygame.draw.rect(surface, "red", self.button_rect)

    def get_value(self):
        # -1 is padding because of pixel precision
        val_range = self.slider_right_pos - self.slider_left_pos - 1
        button_val = self.button_rect.centerx - self.slider_left_pos

        # Get percentage value by pixels by offsetting min
        return (button_val / val_range) * (self.max - self.min) + self.min
