import pygame.mixer_music
from pygame import mixer


def enable_music(enable: bool):
    if enable:
        # Loop background music infinitely
        pygame.mixer.music.play(-1, 0.0)
    else:
        pygame.mixer.music.stop()


def set_music_volume(volume: float):
    if volume > 0:
        pygame.mixer.music.set_volume(volume)
        enable_music(True)
    else:
        enable_music(False)


class AudioPlayer:
    effects_volume = 0.5
    music_volume = 0.3

    mixer.init()

    # Load music and sounds
    pygame.mixer.music.load('app/audio/Combat.mp3')

    sword_hit = pygame.mixer.Sound('app/audio/Sword_hit.wav')
    sword_hit.set_volume(effects_volume)

    potion = pygame.mixer.Sound('app/audio/Potion.wav')
    potion.set_volume(effects_volume)

    sound_effects = [sword_hit, potion]
    set_music_volume(music_volume)

    def set_effects_volume(self, volume: float):
        for sfx in self.sound_effects:
            sfx.set_volume(volume)
