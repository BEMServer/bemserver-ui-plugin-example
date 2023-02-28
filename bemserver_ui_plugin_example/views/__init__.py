"""Plugin views"""
import flask
from pathlib import Path

from . import stats
from ..plugin import PLUGIN_PREFIX


PLUGIN_PATH = Path(__file__).parent.parent


blp = flask.Blueprint(
    PLUGIN_PREFIX,
    __name__,
    url_prefix=f"/{PLUGIN_PREFIX}",
    template_folder=PLUGIN_PATH / "templates",
    static_folder=PLUGIN_PATH / "static" / PLUGIN_PREFIX,
    static_url_path="/static",
)


def register_blueprints(app):
    """Register blueprints"""
    blp.register_blueprint(stats.blp)
    app.register_blueprint(blp)
