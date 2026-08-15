from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import settings


def test_backend_settings_defaults_are_loaded():
    assert settings.PROJECT_NAME
    assert settings.API_V1_STR.startswith("/")
