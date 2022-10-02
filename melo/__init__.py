import os

from melo.configs import APP_DIR
from melo.models import (
    spotify,
    ytmusic,
    youtube
)

__all__ = (
    "spotify",
    "ytmusic",
    "youtube",
)

if not os.path.exists(APP_DIR):
    os.mkdir(APP_DIR)
