
from pathlib import Path

class SaveSystem:
    """Handles saving and loading of game state"""

    def __init__(self, save_directory: str = "saves"):
        self.save_directory = Path(save_directory)

    def load(self, filename = "savename"):
        with open(f"{self.save_directory}/{filename}.txt") as savefile:
            lines = savefile.readlines()
            return lines
    def save(self, filename, text):
        with open(f"{self.save_directory}/{filename}.txt", mode = "w") as savefile:
            for line in text:
                savefile.write(f"{line}\n")