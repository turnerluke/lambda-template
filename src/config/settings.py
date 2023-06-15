import os
import yaml


def unpack_yaml():
    project_root_local = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # For local
    project_root_aws = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # For lambda

    yaml_local = os.path.join(project_root_local, 'config.yaml')
    yaml_aws = os.path.join(project_root_aws, 'config.yaml')
    yaml_path = yaml_local if os.path.exists(yaml_local) else yaml_aws
    #yaml_path = os.path.join(project_root, 'config.yaml')
    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)
    for k, v in config.items():
        os.environ[k] = str(v)


unpack_yaml()
S3_BUCKET = 'ziki-analytics-cleaned-datasets'