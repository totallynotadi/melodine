from melodine import base, spotify, youtube
from melodine import ytmusic

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
