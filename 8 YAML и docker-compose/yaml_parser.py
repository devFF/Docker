# pip install pyyaml
import yaml
import os

if __name__ == '__main__':
    file = os.path.join('8 YAML и docker-compose', "yaml_file.yaml")
    with open(file, 'r') as f:
        templates = yaml.safe_load(f)

    print(templates)