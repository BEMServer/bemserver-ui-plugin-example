"""BEMServer UI plugin"""
from packaging.version import Version


PLUGIN_PREFIX = "example"


PLUGIN_INFO = {
    "label": "A plugin example",
    "description": (
        "A plugin test that adds a sidebar entry in dashboards and display stats"
    ),
    "prefix": PLUGIN_PREFIX,
}


# min <= UI_VERSION < max
REQUIRED_UI_VERSION = {
    "min": Version("0.5.0"),
    "max": Version("0.7.0"),
}


def get_sidebar(campaign_ctxt):
    """Define the plugin sidebar entries that extends application sidebar.
    All the logic about adding an entry to a sidebar section and displaying it
    depending on campaign context is described and customized in this function.

    A sidebar entry is composed of 3 parts: decribed with:
        - an icon, which can be:
            - a bootstrap icon, described by "icon_classes" key
            - or an image, as a plugin "flask.url_for" static endpoint, described by
                "icon_endpoint_kwargs" key containing "endpoint" and "filename" keys
                ("icon_classes" key is optional here)
        - a text, described by "text" key
        - a link, as a plugin "flask.url_for" endpoint, described by "endpoint_kwargs"
            key containing "endpoint" and optionally other specific parameters keys

    Examples of sidebar entry definition:
        1. Simple entry with bootstrap icon and without specific url parameters:
            {
                "icon_classes": ["bi", "bi-123", "text-success"],
                "text": "Data statistics #1",
                "endpoint_kwargs": {"endpoint": f"{PLUGIN_PREFIX}.stats.stats"},
            }

        2. Entry with image icon and specific url parameters:
            {
                "icon_classes": ["bi", "bi-123", "text-success"],  # optional line
                "icon_endpoint_kwargs": {
                    "endpoint": f"{PLUGIN_PREFIX}.static",
                    "filename": "images/bootstrap.svg",
                },
                "text": "Data statistics #2",
                "endpoint_kwargs": {
                    "endpoint": f"{PLUGIN_PREFIX}.stats.stats",
                    "whatever_kwarg": "yep",
                },
            }


    :param CampaignContext campaign_ctxt: Instance of campaign context.

    returns dict that contain a list of entries for sidebar sections.
    """

    sidebar = {
        "dashboards": [],
    }

    # Add an entry that requires a campaign context existence.
    if campaign_ctxt.has_campaign:
        sidebar["dashboards"].append({
            "endpoint_kwargs": {"endpoint": f"{PLUGIN_PREFIX}.stats.stats"},
            "icon_classes": ["bi", "bi-123", "text-success"],
            "text": "Data statistics #1",
        })

    # Add an entry that do not require a campaign context.
    sidebar["dashboards"].append({
        "endpoint_kwargs": {
            "endpoint": f"{PLUGIN_PREFIX}.stats.stats",
            "whatever_kwarg": "yep",
        },
        "icon_endpoint_kwargs": {
            "endpoint": f"{PLUGIN_PREFIX}.static",
            "filename": "images/bootstrap.svg",
        },
        "text": "Data statistics #2",
    })

    return sidebar
