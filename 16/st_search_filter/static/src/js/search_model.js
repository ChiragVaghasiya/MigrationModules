/** @odoo-module **/
import { SearchModel } from "@web/search/search_model";
import { patch } from "@web/core/utils/patch";

const FAVORITE_PRIVATE_GROUP = 1;
const FAVORITE_SHARED_GROUP = 2;

patch(SearchModel.prototype, 'SearchModel', {
    /**
     * override
     */
    async createNewFavorite(params) {
        const { preFavorite, irFilter } = this._getIrFilterDescription(params);
        if (this.env.config && this.env.config.viewType){
            irFilter.context['load_view'] = this.env.config.viewType
        }
        const serverSideId = await this.orm.call("ir.filters", "create_or_replace", [irFilter]);
        this.env.bus.trigger("CLEAR-CACHES");

        // before the filter cache was cleared!
        this.blockNotification = true;
        this.clearQuery();
        const favorite = {
            ...preFavorite,
            type: "favorite",
            id: this.nextId,
            groupId: this.nextGroupId,
            groupNumber: preFavorite.userId ? FAVORITE_PRIVATE_GROUP : FAVORITE_SHARED_GROUP,
            removable: true,
            serverSideId,
        };
        this.searchItems[this.nextId] = favorite;
        this.query.push({ searchItemId: this.nextId });
        this.nextGroupId++;
        this.nextId++;
        this.blockNotification = false;
        this._notify();
        window.location.reload()
    }

});