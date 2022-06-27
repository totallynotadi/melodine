import os

from . import innertube, utils
from .models import *
from .search import search

__all__ = [
    "models.spotify",
    "models.ytmusic",
    "innertube",
    "search",
    "utils"
]

if not os.path.exists(utils.APP_DIR):
    os.mkdir(utils.APP_DIR)
