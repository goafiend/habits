import os
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl
from pathlib import Path
import random
import config
from kivy.core.audio import SoundLoader
class SoundManager:
    def __init__(self, path):
        self.noises = {}
        self.path = path
        self.load_sounds()

    def load_sounds(self):
        path = Path(self.path)
        folders = [f.name for f in path.iterdir() if f.is_dir()]
        for folder_name in folders:
            self.load_noises(folder_name)
    def load_noises(self, name):
        d = []
        self.noises[name] = d
        path = Path(f"{self.path}/{name}")

        file_names = [f.name for f in path.iterdir() if f.is_file()]
        for i in file_names:
            absolute_path = os.path.abspath(f"{path}/{i}")
            sound = SoundLoader.load(absolute_path)
            sound.volume = 0.7
            if config.Sound_manager_prints:
                print(f"sound imported: {absolute_path}")
            d.append(sound)

    def play_noise(self, name):
        sound = random.choice(self.noises[name])
        sound.play()
