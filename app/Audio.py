import pygame.mixer_music
from pygame import mixer

class AudioPlayer:
    mixer.init()

    # Load music and sounds
    pygame.mixer.music.load('app/audio/Combat.mp3')
    pygame.mixer.music.set_volume(0.3)
    # Loop background music infinitely
    pygame.mixer.music.play(-1,0.0)

    sword_hit = pygame.mixer.Sound('app/audio/Sword_hit.wav')
    sword_hit.set_volume(0.5)

    potion = pygame.mixer.Sound('app/audio/Potion.wav')
    potion.set_volume(0.5)