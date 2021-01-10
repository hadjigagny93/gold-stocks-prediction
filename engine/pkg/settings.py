import os

# DEFAULT DIRS
REPO_DIR = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), '..'), '..'))
DATA_DIR = os.path.join(REPO_DIR, 'data/news')
MODELS_DIR = os.path.join(REPO_DIR, "engine/pkg/models/")


# DATABASE SETTINGS
DATABASES = {
        'database': os.getenv("DB_NAME"),
        'user': os.getenv("DB_USER"),
        'password': os.getenv("DB_PASSWORD"),
        'host': os.getenv("DB_HOST"),
        'port': os.getenv("DB_PORT"),
}
