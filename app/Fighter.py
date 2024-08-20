import pygame
from .Drawing import red, green


class Fighter:
    def __load_images(self, action_name):
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'app/img/{self.name}/{action_name}/{i}.png')
            # This is for up scaling the image, because it's too small, scaling three times in each direction
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potions = potions
        self.potions = potions
        self.alive = True

        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0-Idle, 1-Attack, 2-Hurt, 3-Dead
        self.update_time = pygame.time.get_ticks()
        # Load images
        self.__load_images('Idle')
        self.__load_images('Attack')
        # self.__load_images('Hurt')
        # self.__load_images('Death')

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()  # Invisible property that shows width and height of image
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 100
        # Handle animation
        # Update Image
        self.image = self.animation_list[self.action][self.frame_index]
        # if difference between current time and time since last update is greater than cooldown then update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if animation reaches the end then restart
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class HealthBar:
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp, screen):
        # Update with new health
        self.hp = hp
        # Calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))
