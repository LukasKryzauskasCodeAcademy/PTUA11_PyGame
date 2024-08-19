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

        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        for i in range(8):
            img = pygame.image.load(f'app/img/{self.name}/Idle/{i}.png')
            # This is for up scaling the image, because it's too small, scaling three times in each direction
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()  # Invisible property that shows width and height of image
        self.rect.center = (x, y)

    def update(self):
        animation_cooldown = 100
        # Handle animation
        # Update Image
        self.image = self.animation_list[self.frame_index]
        # if difference between current time and time since last update is greater than cooldown then update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if animation reaches the end then restart
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)
