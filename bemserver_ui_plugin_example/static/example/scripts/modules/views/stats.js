// Import modules from BEMServer UI ("/static/...").
import { flaskES6 } from "/static/scripts/app.js";
import { InternalAPIRequest } from "/static/scripts/modules/tools/fetcher.js";
import { FlashMessageTypes, FlashMessage } from "/static/scripts/modules/components/flash.js";
import { Spinner } from "/static/scripts/modules/components/spinner.js";
import "/static/scripts/modules/components/eventLevel.js";


export class StatsView {

    #internalAPIRequester = null;
    #getReqID = null;

    #messagesElmt = null;
    #getBtnElmt = null;
    #getBtnLoadingElmt = null;

    constructor() {
        this.#internalAPIRequester = new InternalAPIRequest();
    }

    #cacheDOM() {
        this.#messagesElmt = document.getElementById("messages");
        this.#getBtnElmt = document.getElementById("getBtn");
        this.#getBtnLoadingElmt = document.getElementById("getBtnLoading");
    }

    #initEventListeners() {
        this.#getBtnElmt.addEventListener("click", (event) => {
            event.preventDefault();

            this.#getBtnLoadingElmt.innerHTML = "";
            this.#getBtnLoadingElmt.appendChild(new Spinner({ useSmallSize: true }));

            if (this.#getReqID != null) {
                this.#internalAPIRequester.abort(this.#getReqID);
                this.#getReqID = null;
            }

            this.#getReqID = this.#internalAPIRequester.get(
                flaskES6.urlFor(`api.notifications.retrieve_count`, {read: false}),
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

                    let flashMsgElmt = new FlashMessage({type: FlashMessageTypes.INFO, text: msgContent, isDismissible: true, isTimed: false});
                    this.#messagesElmt.appendChild(flashMsgElmt);
                },
                (error) => {
                    let flashMsgElmt = new FlashMessage({type: FlashMessageTypes.ERROR, text: error.toString(), isDismissible: true});
                    this.#messagesElmt.appendChild(flashMsgElmt);
                },
                () => {
                    this.#getBtnLoadingElmt.innerHTML = "";
                },
            );
        });
    }

    mount() {
        this.#cacheDOM();
        this.#initEventListeners();
    }
}
