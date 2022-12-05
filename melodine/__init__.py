from melodine import player
from melodine.models import (
    base,
    spotify,
    ytmusic,
    youtube
)

__all__ = (
    "base",
    "spotify",
    "ytmusic",
    "youtube",
    'player',
)

from melodine.configs import APP_DIR
import os
if not os.path.exists(APP_DIR):
    os.mkdir(APP_DIR)
