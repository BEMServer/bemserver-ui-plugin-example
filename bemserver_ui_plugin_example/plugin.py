"""BEMServer UI plugin"""
from packaging.version import Version


PLUGIN_PREFIX = "example"


PLUGIN_INFO = {
    "label": "A plugin example",
    "description": (
        "A plugin test that adds a sidebar entry in dashboards and display stats"
    ),
    "prefix": PLUGIN_PREFIX,
    "sidebar": {
        "tsdata": [],
        "analysis": [],
        "services": [],
        "dashboards": [
            {
                "endpoint_kwargs": {"endpoint": f"{PLUGIN_PREFIX}.stats.stats"},
                "icon_classes": ["bi", "bi-123", "text-success"],
                "text": "Data statistics #1",
                "requires_campaign_context": True,
            },
            {
                "endpoint_kwargs": {
                    "endpoint": f"{PLUGIN_PREFIX}.stats.stats",
                    "whatever_kwarg": "yep",
                },
                "icon_endpoint_kwargs": {
                    "endpoint": f"{PLUGIN_PREFIX}.static",
                    "filename": "images/bootstrap.svg",
                },
                "text": "Data statistics #2",
                "requires_campaign_context": False,
            },
        ],
    },
}


# min <= UI_VERSION < max
REQUIRED_UI_VERSION = {
    "min": Version("0.4.0"),
    "max": Version("0.5.0"),
}
