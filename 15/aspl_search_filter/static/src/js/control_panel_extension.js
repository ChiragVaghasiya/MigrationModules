
odoo.define('aspl_search_filter.control_panel_extension_test', function (require) {
    "use strict";

    var ControlPanelModelExtension = require('web/static/src/js/control_panel/control_panel_model_extension.js');

    /**
     * override
     */
    // Reload page once favorite created.
    async function createNewFavorite(preFilter) {
        const preFavorite = await this._saveQuery(preFilter);
        this.clearQuery();
        const filter = Object.assign(preFavorite, {
            groupId: this.state.nextGroupId,
            id: this.state.nextId,
        });
        this.state.filters[this.state.nextId] = filter;
        this.state.query.push({ groupId: this.state.nextGroupId, filterId: this.state.nextId });
        this.state.nextGroupId++;
        this.state.nextId++;
        window.location.reload()
    }

    /**
     * override
     */
    // Include context with a filter when creating a favorite
    async function _saveQuery(preFilter) {
        const irFilter = this.getIrFilterValues(preFilter);
        var url = self.location.href
        var view_type = getUrlParameter(url, 'view_type');

        if (view_type){
            irFilter.context['load_view'] = view_type
        }

        function getUrlParameter(url, parameterName) {
            parameterName = parameterName.replace(/[\[\]]/g, "\\$&");
            var regex = new RegExp("[?#&]" + parameterName + "(=([^&#]*)|&|#|$)");
            var results = regex.exec(url);
            if (!results) return null;
            if (!results[2]) return '';
            return decodeURIComponent(results[2].replace(/\+/g, " "));
        }
        const serverSideId = await this.env.dataManager.create_filter(irFilter);

        preFilter.serverSideId = serverSideId;
        return preFilter;
    }

    
    ControlPanelModelExtension.prototype.createNewFavorite = createNewFavorite;
    ControlPanelModelExtension.prototype._saveQuery = _saveQuery;
    return ControlPanelModelExtension;

});
