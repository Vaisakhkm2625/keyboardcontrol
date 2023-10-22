import yaml

config_path = "/home/vaisakh/.config/keyboardcontrol/default.yml"

with open(config_path) as file:
    config = yaml.safe_load(file)


os="linux"
platform="hyprland"


for k,v in config["general"].items():
    print(f" {v.name} {v['desc']} ")
    print(config["general"][k][os][platform]['cmd'])
    print()


