import yaml
import subprocess
import glob
import keyboard

class ConfigurationRunner:
    def __init__(self, os, platform, config_path):
        self.os = os
        self.platform = platform
        self.config_path = config_path

    def read_yaml_file(self, filename):
        with open(filename, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def execute_command(self, shell_command):
        try:
            returned_out = subprocess.check_output(shell_command, shell=True)
            print(returned_out)
        except Exception as e:
            print(f"Error executing the command: {e}")

    def load_configurations(self):
        files = glob.glob(self.config_path, recursive=True)
        data = []
        for file in files:
            data.append(self.read_yaml_file(file))
        return data

    def register_hotkeys(self, configurations):
        for config in configurations:
            hotkey = config["keybinding"].lower()
            desc = config["desc"]
            cmd = config["supported_os"][self.os][self.platform]["cmd"]
            keyboard.add_hotkey(hotkey, lambda: self.execute_command(cmd))
            print(f"Registered hotkey: {hotkey} - {desc}")

    def run(self):
        configurations = self.load_configurations()
        self.register_hotkeys(configurations)
        keyboard.wait('esc')

if __name__ == "__main__":
    os = "linux"
    platform = "hyprland"
    userConfigPath = "/home/vaisakh/vaisakhRoot/programming/python/keyboardcontrol/config/**/*.yml"

    config_manager = ConfigurationManager(os, platform, userConfigPath)
    config_manager.run()
