import json
import os.path

class SaveFile:
    def __init__(self):
        self.save_data = {
            'music_volume': 0.5,
            'effects_volume': 0.3
        }
        # Load initial save info if it exists.
        self.load()

    def save(self):
        with open('save.txt', 'w') as test_file:
            json.dump(self.save_data, test_file)

    def load(self):
        if os.path.isfile('save.txt'):
            with open('save.txt') as test_file:
                self.save_data = json.load(test_file)
                for entry in self.save_data:
                    print(entry)
