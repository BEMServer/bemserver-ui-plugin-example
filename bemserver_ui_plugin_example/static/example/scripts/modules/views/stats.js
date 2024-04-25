// Import modules from BEMServer UI ("/static/...").
import { app } from "/static/scripts/app.js";
import { InternalAPIRequest } from "/static/scripts/modules/tools/fetcher.js";
import { Spinner } from "/static/scripts/modules/components/spinner.js";
import "/static/scripts/modules/components/eventLevel.js";


class StatsView {

    #internalAPIRequester = null;
    #getReqID = null;

    #getBtnElmt = null;
    #getBtnLoadingElmt = null;

    constructor() {
        this.#internalAPIRequester = new InternalAPIRequest();
    }

    #cacheDOM() {
        this.#getBtnElmt = document.getElementById("getBtn");
        this.#getBtnLoadingElmt = document.getElementById("getBtnLoading");
    }

    #initEventListeners() {
        this.#getBtnElmt.addEventListener("click", (event) => {
            event.preventDefault();

            this.#getBtnLoadingElmt.innerHTML = "";
            this.#getBtnLoadingElmt.appendChild(new Spinner({ useSmallSize: true }));

            this.#getBtnElmt.setAttribute("disabled", true);

            if (this.#getReqID != null) {
                this.#internalAPIRequester.abort(this.#getReqID);
                this.#getReqID = null;
            }

            this.#getReqID = this.#internalAPIRequester.get(
                app.urlFor(`api.notifications.retrieve_count`, {read: false}),
                (data) => {
                    let msgContent = `<p>No <span class="fw-bold">unread</span> notifications.</p>`;
                    if (data.data.total > 0) {
                        msgContent = `<p class="mb-0">Campaign notifications (${data.data.total} overall):</p>`;
                        msgContent += `<ul class="mb-0">`;
                        for (let campaignNotifsData of data.data.campaigns) {
                            msgContent += `<li><span class="fw-bold">${campaignNotifsData.campaign_name}</span> has <span class="fw-bold">${campaignNotifsData.count}</span> unread notification${campaignNotifsData.count > 1 ? "s": ""}</li>`;
                        }
                        msgContent += `</ul>`;
                    }

                    app.flashMessage(msgContent, "info");
                },
                (error) => {
                    app.flashMessage(error.toString(), "error");
                },
                () => {
                    this.#getBtnLoadingElmt.innerHTML = "";
                    this.#getBtnElmt.removeAttribute("disabled");
                },
            );
        });
    }

    mount() {
        this.#cacheDOM();
        this.#initEventListeners();
    }
}


document.addEventListener("DOMContentLoaded", () => {
    let view = new StatsView();
    view.mount();
});
