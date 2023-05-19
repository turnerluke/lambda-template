import os
import yaml

def unpack_yaml():
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    for k, v in config.items():
        os.environ[k] = str(v)

unpack_yaml()