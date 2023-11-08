
import yaml
import subprocess
import glob
import keyboard

class ConfigLoader:
    def __init__(self, config_path, os, platform):
        self.config_path = config_path
        self.os = os
        self.platform = platform
        self.data = []

    def read_yaml_file(self, filename):
        with open(filename, 'r') as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def load_configs(self):
        files = glob.glob(self.config_path, recursive=True)
        for file in files:
            config = self.read_yaml_file(file)
            self.data.append(config)


class CommandExecutor:
    def execute_command(self, shell_command):
        try:
            subprocess.Popen(shell_command.split(" "), shell=True)
        except Exception as e:
            print(f"Error executing the command: {e}")



class HotkeyHandler:
    def __init__(self):
        self.handlers = []

    def add_hotkey(self, hotkey, command):
        keyboard.add_hotkey(hotkey.lower(), command)

    def wait_for_exit(self):
        keyboard.wait('esc')




if __name__ == "__main__":
    os = "linux"
    platform = "hyprland"
    userConfigPath = "../config/**/*.yml"

    config_loader = ConfigLoader(userConfigPath, os, platform)
    config_loader.load_configs()

    command_executor = CommandExecutor()

    hotkey_handler = HotkeyHandler()

    for config in config_loader.data:
        hotkey = config["keybinding"]
        desc = config["desc"]
        cmd = config["supported_os"][os][platform]["cmd"]

        def create_command_executor(cmd):
            return lambda: command_executor.execute_command(cmd)

        hotkey_handler.add_hotkey(hotkey, create_command_executor(cmd))

    hotkey_handler.wait_for_exit()
