from functools import lru_cache
from pathlib import Path

from dynaconf import Dynaconf, LazySettings

BASE_DIR: Path = Path(__file__).resolve().parent.parent

settings: LazySettings = Dynaconf(
    settings_files=[BASE_DIR / "core/settings.yaml", BASE_DIR / "core/.secrets.yaml"],
    environments=True,
    load_dotenv=True,
    dotenv_path=BASE_DIR / ".env",
)


@lru_cache
def get_settings():
    return settings
