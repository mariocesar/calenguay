from .base import *

DEBUG = True

INSTALLED_APPS = [
    *INSTALLED_APPS,
    "livereload"
]

MIDDLEWARE = [
    *MIDDLEWARE,
    "livereload.middleware.LiveReloadScript",
]
