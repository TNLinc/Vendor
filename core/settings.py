from pathlib import Path

from environs import Env

env = Env()
env.read_env(".env")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

PROJECT_NAME = "Vendor"
DB_URL = env("VENDOR_DB_URL")

VENDOR_ALLOWED_HOSTS = env.list("VENDOR_ALLOWED_HOSTS", default=['*'])

DB_AUTH_SCHEMA = env("VENDOR_DB_AUTH_SCHEMA")
