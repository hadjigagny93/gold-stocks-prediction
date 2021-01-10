# This script enables docker env detection
import os

def is_dot_docker_env_there():
    root_dir_content = os.listdir('/')
    return '.dockerenv' in root_dir_content


if __name__ == "__main__":
    print(is_dot_docker_env_there())
