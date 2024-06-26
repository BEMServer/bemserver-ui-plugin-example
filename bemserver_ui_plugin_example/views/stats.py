"""Stats page"""

import flask

from bemserver_ui.extensions import auth
from bemserver_ui.common.const import FULL_STRUCTURAL_ELEMENT_TYPES

from ..plugin import PLUGIN_PREFIX


blp = flask.Blueprint("stats", __name__, url_prefix="/stats")


@blp.route("/")
@auth.signin_required
def stats():
    campaign_scopes_count_overall = 0
    cs_resp = flask.g.api_client.campaign_scopes.getall()
    campaign_scopes_count_overall = len(cs_resp.data)

    campaign_scopes_count = 0
    if flask.g.campaign_ctxt.has_campaign:
        cs_resp = flask.g.api_client.campaign_scopes.getall(
            campaign_id=flask.g.campaign_ctxt.id,
        )
        campaign_scopes_count = len(cs_resp.data)

    ts_count_overall = 0
    ts_resp = flask.g.api_client.timeseries.getall(page_size=1)
    ts_count_overall = ts_resp.pagination["total"]

    ts_count = 0
    if flask.g.campaign_ctxt.has_campaign:
        ts_resp = flask.g.api_client.timeseries.getall(
            page_size=1,
            campaign_id=flask.g.campaign_ctxt.id,
        )
        ts_count = ts_resp.pagination["total"]

    struct_elmt_count_overall = {x: 0 for x in FULL_STRUCTURAL_ELEMENT_TYPES}
    struct_elmt_count = {x: 0 for x in FULL_STRUCTURAL_ELEMENT_TYPES}
    for struct_elmt_type in FULL_STRUCTURAL_ELEMENT_TYPES:
        api_resource = getattr(flask.g.api_client, f"{struct_elmt_type}s")
        struct_elmt_resp = api_resource.getall()
        struct_elmt_count_overall[struct_elmt_type] = len(struct_elmt_resp.data)
        if flask.g.campaign_ctxt.has_campaign:
            struct_elmt_resp = api_resource.getall(
                campaign_id=flask.g.campaign_ctxt.id,
            )
            struct_elmt_count[struct_elmt_type] = len(struct_elmt_resp.data)

    return flask.render_template(
        f"{PLUGIN_PREFIX}/stats.html",
        plugin_prefix=PLUGIN_PREFIX,
        campaign_scopes_count_overall=campaign_scopes_count_overall,
        campaign_scopes_count=campaign_scopes_count,
        ts_count_overall=ts_count_overall,
        ts_count=ts_count,
        structural_element_types=FULL_STRUCTURAL_ELEMENT_TYPES,
        structural_element_count_overall=struct_elmt_count_overall,
        structural_element_count=struct_elmt_count,
    )
