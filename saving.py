
from pathlib import Path
from kivy.app import App
import json

class SaveSystem:
    """Handles saving and loading of game state"""

    def __init__(self, save_directory: str = "saves"):
        # user_data_dir resolves to the correct sandboxed path per platform:
        # Android: /data/data/<appname>/files/
        # iOS:     <AppHome>/Documents/
        # Desktop: ~/.appname/
        base = Path(App.get_running_app().user_data_dir)
        print(base.absolute())
        self.save_directory = base / save_directory
        self.save_directory.mkdir(parents=True, exist_ok=True)

    def load(self, filename = "savename"):
        path = self.save_directory / f"{filename}.json"
        if not path.exists():
            return None, None
        with open(path) as f:
            payload = json.load(f)
        return payload
    def save(self, filename, data_dict):
        with open(f"{self.save_directory}/{filename}.json", "w") as savefile:
            print(f"{data_dict=}")
            json.dump(data_dict, savefile, indent=2)
