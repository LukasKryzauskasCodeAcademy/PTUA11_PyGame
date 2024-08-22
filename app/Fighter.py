import pygame
import random
from .Drawing import red, green, DamageText


class Fighter:
    def __load_images(self, action_name, frames):
        temp_list = []
        for i in range(frames):
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
        self.__load_images('Idle', 8)
        self.__load_images('Attack', 8)
        self.__load_images('Hurt', 3)
        self.__load_images('Death', 10)

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
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.animation(0)

    def animation(self, action):
        # set variables for animation, action determines the animation, 0-Idle, 1-Attack, 2-Hurt, 3-Dead
        self.action = action
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        from app import damage_text_group

        rand = random.randint(-5, 5)
        damage = self.strength + rand
        # Deal damage to enemy
        target.hp -= damage
        # Run enemy hurt animation
        target.animation(2)
        # Check if target is dead
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.animation(3)
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)
        # Set variables to attack animation
        self.animation(1)

    def reset(self):
        self.alive = True
        self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

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
