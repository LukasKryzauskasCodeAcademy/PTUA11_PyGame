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
    sword_hit = None
    potion = None
    sound_effects = None

    def __init__(self, music_volume: float, effects_volume: float):
        self.music_volume = music_volume
        self.effects_volume = effects_volume

        #Load up audio
        mixer.init()
        self.load_audio()

    # Load music and sounds
    def load_audio(self):
        pygame.mixer.music.load('app/audio/Combat.mp3')

        self.sword_hit = pygame.mixer.Sound('app/audio/Sword_hit.wav')
        self.sword_hit.set_volume(self.effects_volume)

        self.potion = pygame.mixer.Sound('app/audio/Potion.wav')
        self.potion.set_volume(self.effects_volume)

        self.sound_effects = [self.sword_hit, self.potion]
        set_music_volume(self.music_volume)

    def set_effects_volume(self, volume: float):
        for sfx in self.sound_effects:
            sfx.set_volume(volume)
