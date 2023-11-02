import yaml,os
import subprocess
import glob,keyboard

os = "linux"
platform = "hyprland"

def read_yaml_file(filename):
    with open(filename, 'r') as stream:
        try:
            #print(yaml.safe_load(stream))
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


files = glob.glob("/home/vaisakh/vaisakhRoot/programming/python/keyboardcontrol/config/**/*.yml",recursive=True) # list of all .yaml files in a directory 

def execute_command(shell_command):
    try:
        #returned = subprocess.run(shell_command, shell=True)
        returned_out = subprocess.check_output(shell_command, shell=True)
        print(returned_out)
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


