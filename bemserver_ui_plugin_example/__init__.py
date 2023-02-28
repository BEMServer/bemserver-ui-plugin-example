"""BEMServer UI plugin"""
from . import views
from .plugin import PLUGIN_INFO, REQUIRED_UI_VERSION  # noqa


__version__ = "0.1.0"


def init_app(app):
    """Init plugin in app"""
    views.register_blueprints(app)
