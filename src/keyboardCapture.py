
import yaml
import subprocess
import glob
import keyboard

class ConfigLoader:
    def __init__(self, config_path, os, platform):
        self.config_path = config_path+"**/*.yml"
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

class KeyboardController:
    def __init__(self, config_path, os, platform):
        self.config_loader = ConfigLoader(config_path, os, platform)
        self.command_executor = CommandExecutor()
        self.hotkey_handler = HotkeyHandler()

    def setup(self):
        self.config_loader.load_configs()

        for config in self.config_loader.data:
            hotkey = config["keybinding"]
            desc = config["desc"]
            cmd = config["supported_os"][self.config_loader.os][self.config_loader.platform]["cmd"]

            def create_command_executor(cmd):
                return lambda: self.command_executor.execute_command(cmd)

            self.hotkey_handler.add_hotkey(hotkey, create_command_executor(cmd))

    def run(self):
        self.hotkey_handler.wait_for_exit()

    def stop(self):
            keyboard.unhook_all()

if __name__ == "__main__":
    os = "linux"
    platform = "hyprland"
    userConfigPath = "../config/**/*.yml"

    app = KeyboardController(userConfigPath, os, platform)
    app.setup()
    app.run()
