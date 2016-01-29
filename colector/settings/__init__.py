# application_python cookbook expects manage.py in a top level
# instead of app level dir, so the relative import can fail
try:
    from .colector.colector.settings.base import *
except ImportError:
    from colector.settings.base import *


try:
    from local_settings import *
except ImportError:
    pass