from melodine import base, spotify, youtube, ytmusic

__all__ = (
    "base",
    "spotify",
    "ytmusic",
    "youtube",
)

import os

from melodine.configs import APP_DIR

if not os.path.exists(APP_DIR):
    os.mkdir(APP_DIR)
