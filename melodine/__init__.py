from melodine import base, spotify, ytmusic, youtube

__all__ = (
    "base",
    "spotify",
    "ytmusic",
    "youtube",
)

from melodine.configs import APP_DIR
import os

if not os.path.exists(APP_DIR):
    os.mkdir(APP_DIR)
