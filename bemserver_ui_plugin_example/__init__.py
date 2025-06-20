"""BEMServer UI plugin"""

from . import views
from .plugin import PLUGIN_INFO, REQUIRED_UI_VERSION, get_sidebar  # noqa


__version__ = "0.2.3"


def init_app(app):
    """Init plugin in app"""
    views.register_blueprints(app)
