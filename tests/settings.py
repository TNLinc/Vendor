from pathlib import Path

from environs import Env

env = Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
TEST_DIR = Path(__file__).resolve().parent
env.read_env(str(TEST_DIR / ".env.test"))

PROJECT_NAME = "Vendor"

TEST_DB_URL = env("TEST_DB_URL")

VENDOR_ALLOWED_HOSTS = env.list("VENDOR_ALLOWED_HOSTS", default=["*"])

DB_AUTH_SCHEMA = env("VENDOR_DB_SCHEMA")
