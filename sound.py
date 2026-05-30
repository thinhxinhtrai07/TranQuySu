import os

import pygame


class SoundManager:

    """Quan ly am thanh cua game.

    Project hien chi dung cac file MP3 sau:
    - Music: assets/music/menu.mp3, assets/music/stage1.mp3
    - SFX: attack.mp3, heal.mp3, death.mp3, skill_q.mp3, skill_e.mp3, skill_f.mp3
    """


    MUSIC_FILES = {

        'menu': 'menu.mp3',

        'stage1': 'stage1.mp3',

    }


    SOUND_FILES = {

        'attack': 'attack.mp3',

        'heal': 'heal.mp3',

        'death': 'death.mp3',

        'q': 'skill_q.mp3',

        'e': 'skill_e.mp3',

        'f': 'skill_f.mp3',

    }


    def __init__(self, settings):

        self.settings = settings

        self.current_music = None

        self.current_music_key = None

        self.sounds = {}

        self.audio_ready = False

        self._init_mixer()

        self._load_sounds()


    def _init_mixer(self):

        try:

            if not pygame.mixer.get_init():

                pygame.mixer.init()

            pygame.mixer.set_num_channels(32)

            self.audio_ready = True

        except pygame.error:

            self.audio_ready = False


    def muted(self):

        return bool(self.settings.get('mute', False))


    def _music_path(self, name):

        filename = self.MUSIC_FILES.get(name)

        if not filename:

            return None

        path = os.path.join(os.path.dirname(__file__), 'assets', 'music', filename)

        return path if os.path.exists(path) else None


    def _load_sounds(self):

        if not self.audio_ready:

            return

        base = os.path.join(os.path.dirname(__file__), 'assets', 'sounds')

        for key, filename in self.SOUND_FILES.items():

            path = os.path.join(base, filename)

            self.sounds[key] = self._load_sound_file(path)

        self.apply_settings()


    def _load_sound_file(self, path):

        if not os.path.exists(path):

            return None

        try:

            return pygame.mixer.Sound(path)

        except pygame.error:

            return None


    def apply_settings(self):

        if not self.audio_ready:

            return


        music_volume = 0.0 if self.muted() else float(self.settings.get('music_volume', 0.5))

        sfx_volume = 0.0 if self.muted() else float(self.settings.get('sfx_volume', 0.7))

        music_volume = max(0.0, min(1.0, music_volume))

        sfx_volume = max(0.0, min(1.0, sfx_volume))


        try:

            pygame.mixer.music.set_volume(music_volume)

        except pygame.error:

            pass


        for sound in self.sounds.values():

            if sound is not None:

                sound.set_volume(sfx_volume)


    def _play_sound(self, key):

        if not self.audio_ready or self.muted():

            return None


        sound = self.sounds.get(key)

        if sound is None:

            return None


        try:

            sfx_volume = float(self.settings.get('sfx_volume', 0.7))

            sfx_volume = max(0.0, min(1.0, sfx_volume))

            channel = pygame.mixer.find_channel(True)

            if channel is not None:

                channel.set_volume(sfx_volume)

                channel.play(sound)

            else:

                sound.set_volume(sfx_volume)

                sound.play()

        except pygame.error:

            return None

        return None


    def play_attack_sound(self):

        return self._play_sound('attack')


    def play_skill_sound(self, name='q'):

        key = str(name).lower()

        if key not in self.SOUND_FILES:

            key = 'attack'

        return self._play_sound(key)


    def play_heal_sound(self):

        return self._play_sound('heal')


    def play_death_sound(self):

        return self._play_sound('death')


    def play_background_music(self, name='menu', volume=None):

        self.current_music_key = name

        if not self.audio_ready:

            return None


        path = self._music_path(name)

        if path is None:

            return None


        desired_volume = float(self.settings.get('music_volume', 0.5) if volume is None else volume)

        desired_volume = 0.0 if self.muted() else max(0.0, min(1.0, desired_volume))


        if self.current_music == path:

            try:

                pygame.mixer.music.set_volume(desired_volume)

                if not pygame.mixer.music.get_busy() and not self.muted():

                    pygame.mixer.music.play(-1)

            except pygame.error:

                return None

            return None


        try:

            pygame.mixer.music.load(path)

            pygame.mixer.music.set_volume(desired_volume)

            self.current_music = path

            if not self.muted():

                pygame.mixer.music.play(-1)

        except pygame.error:

            self.current_music = None

        return None


    def stop_background_music(self):

        if not self.audio_ready:

            self.current_music = None

            return

        try:

            pygame.mixer.music.stop()

        except pygame.error:

            pass

        self.current_music = None

