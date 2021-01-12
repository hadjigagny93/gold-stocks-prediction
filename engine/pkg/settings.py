import os

# DEFAULT DIRS
REPO_DIR = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), '..'), '..'))
DATA_DIR = os.path.join(REPO_DIR, 'data/news')
MODELS_DIR = os.path.join(REPO_DIR, "engine/pkg/models/")
