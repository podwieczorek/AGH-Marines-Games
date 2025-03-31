import json
import os


class Settings:
    def __init__(self, settings_file):
        self.settings_file = settings_file
        self.s = {}
        self.load_settings()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as file:
                self.s = json.load(file)
        else:
            self.s = {}

    def save_settings(self):
        with open(self.settings_file, 'w') as file:
            json.dump(self.s, file, indent=4)

    def get_setting(self, key, default=None):
        return self.s.get(key, default)

    def set_setting(self, key, value):
        print(os.path.relpath(__file__))
        self.s[key] = value
        self.save_settings()
