/** @odoo-module **/
import { FavoriteMenu } from "@web/search/favorite_menu/favorite_menu";
import { patch } from "@web/core/utils/patch";


patch(FavoriteMenu.prototype, 'FavoriteMenu', {
    /**
     * override
     */
    onFavoriteSelected(itemId) {
        this.env.searchModel.toggleSearchItem(itemId);
        const searchItem = this.env.searchModel.searchItems[itemId];
        if(searchItem && searchItem.context && searchItem.context.load_view == 'list'){
            $('.o_list').click();
        }
        else if(searchItem && searchItem.context && searchItem.context.load_view == 'kanban'){
            $('.o_kanban').click();
        }
        else if(searchItem && searchItem.context && searchItem.context.load_view == 'calendar'){
            $('.o_calendar').click();
        }
        else if(searchItem && searchItem.context && searchItem.context.load_view == 'pivot'){
            $('.o_pivot').click();
        }
        else if(searchItem && searchItem.context && searchItem.context.load_view == 'graph'){
            $('.o_graph').click();
        }
        else if(searchItem && searchItem.context && searchItem.context.load_view == 'activity'){
            $('.o_activity').click();
        }
        else if(searchItem && searchItem.context && searchItem.context.load_view == 'gantt'){
            $('.o_gantt').click();
        }
    }
});