import pygame


class Player():
    def __init__(self):
        self.song = None
        self.is_paused = False

    def change_song(self, songplace:str):
        """
        Смена песни

        Args:
            songplace (str): Путь к песни
        """
        pygame.mixer.music.stop()
        pygame.mixer.music.load(songplace)
        self.song = songplace
        pygame.mixer.music.play()
        self.is_paused = False

    def stop(self):
        """
        Остановить проигрывание песни
        """
        pygame.mixer.music.stop()
        self.is_paused = False

    def pause(self):
        """
        Пауза песни
        """
        pygame.mixer.music.pause()
        self.is_paused = True

    def play(self)->None:
        """
        Продолжить воспроизведение песни/начать его
        """
        if self.is_paused:
            pygame.mixer.music.unpause()
        elif self.song is not None:
            pygame.mixer.music.play()
            