import yaml,os
import subprocess
import glob,keyboard
#from PyQt6.QtCore import QStandardPaths

os = "linux"
platform = "hyprland"

def read_yaml_file(filename):
    with open(filename, 'r') as stream:
        try:
            #print(yaml.safe_load(stream))
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


#configLocation = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.ConfigLocation)
#userConfigPath = configLocation+"/keyboardcontrol"
#userConfigPath = "/home/vaisakh/vaisakhRoot/programming/python/keyboardcontrol/config/**/*.yml"
userConfigPath = "../config/**/*.yml"
files = glob.glob(userConfigPath,recursive=True) # list of all .yaml files in a directory 

def execute_command(shell_command):
    try:
        subprocess.Popen(shell_command.split(" "), shell=True)
    except Exception as e:
        print(f"Error executing the command: {e}")


data = []
for file in files:
    data.append(read_yaml_file(file))


for config in data:
    #print(config)

    hotkey = config["keybinding"]
    desc =  config["desc"]
    cmd =  config["supported_os"][os][platform]["cmd"]
    print(hotkey,desc,cmd)

    keyboard.add_hotkey(hotkey.lower(), lambda: execute_command(cmd))

keyboard.wait('esc')
