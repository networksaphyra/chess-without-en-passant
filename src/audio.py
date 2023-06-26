from chessConfiguration import Configuration
import pygame

class Audio:
    def __init__(self):
        """
        Initializes the Audio object.

        Loads the audio files and initializes the mixer.
        """
        pygame.mixer.init()
        self.config = Configuration()
        self.audio_files = {
            'capture': self.config.get_path('capture'),
            'castle': self.config.get_path('castle'),
            'check': self.config.get_path('check'),
            'game': self.config.get_path('game'),
            'move': self.config.get_path('move'),
            'promote': self.config.get_path('promote')
        }

    def play_capture(self):
        """
        Plays the capture sound effect.
        """
        self._play_audio('capture')

    def play_castle(self):
        """
        Plays the castle sound effect.
        """
        self._play_audio('castle')

    def play_check(self):
        """
        Plays the check sound effect.
        """
        self._play_audio('check')

    def play_game(self):
        """
        Plays the game sound effect.
        """
        self._play_audio('game')

    def play_move(self):
        """
        Plays the move sound effect.
        """
        self._play_audio('move')

    def play_promote(self):
        """
        Plays the promote sound effect.
        """
        self._play_audio('promote')

    def _play_audio(self, audio_name):
        """
        Plays the specified audio file.

        Args:
            audio_name (str): The name of the audio file.
        """
        audio_path = self.audio_files.get(audio_name)
        if audio_path:
            pygame.mixer.music.load(str(audio_path))
            pygame.mixer.music.play()
