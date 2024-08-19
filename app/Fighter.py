import pygame


class Fighter:
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True
        img = pygame.image.load(f'app/img/{self.name}/Idle/0.png')
        # This is for up scaling the image, because it's too small, scaling three times in each direction
        self.image = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
        self.rect = self.image.get_rect()  # Invisible property that shows width and height of image
        self.rect.center = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
