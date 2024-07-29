import json
import os

from src.util.modifiers import Modifiers


class Config:
    _instance = None
    config_file = os.path.dirname(__file__) + "/config.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        if not os.path.isfile(self.config_file):
            self.__warn("Config file not found!")
            self.config_map = {}
            self.setup_config_file()

        with open(self.config_file, 'r') as file:
            self.config_map = json.load(file)

    def setup_config_file(self):
        print(Modifiers.BOLD + "Setting up config file!" + Modifiers.NORMAL)

        self.__read_value("INTERVAL", int,
                          "Enter the interval (in terms of seconds) that will be used in watch mode")
        self.__read_value("PROD_CONTEXT", str, "Enter the production context for k8s")
        self.__read_value("DEV_CONTEXT", str, "Enter the development context for k8s")
        self.__read_value("DEFAULT_NAMESPACE", str, "Enter the default namespace for k8s")

        with open(self.config_file, 'w') as file:
            file.write(json.dumps(self.config_map))

    def __read_value(self, config_key: str, map_function: type, text: str):
        current_value = self.config_map.get(config_key, None)
        text = Modifiers.BOLD + text + Modifiers.NORMAL
        if current_value:
            text += Modifiers.DIMMED + f"\n(Enter for using existing value: {current_value})" + Modifiers.NORMAL
        text += " >>> "

        print()
        while True:
            value = input(text)
            if value == "":
                if current_value is None:
                    self.__warn("Value cannot be empty!")
                else:
                    break
            else:
                try:
                    self.config_map[config_key] = map_function(value)
                    break
                except ValueError as e:
                    self.__warn(f"Given value must be {map_function.__name__}")

    def get(self, key, default=None):
        return self.config_map.get(key, default)

    @staticmethod
    def __warn(text: str):
        print(Modifiers.YELLOW + text + Modifiers.NORMAL)


config = Config()
