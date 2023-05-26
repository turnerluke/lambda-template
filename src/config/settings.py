import os
import yaml


def unpack_yaml():
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    yaml_path = os.path.join(project_root, 'config.yaml')
    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)
    for k, v in config.items():
        os.environ[k] = str(v)


unpack_yaml()
S3_BUCKET = 'ziki-analytics-cleaned-datasets'