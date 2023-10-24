
odoo.define('aspl_save_view_to_favourite.cp_favourite_menu', function (require) {
    "use strict";

    var FavouriteMenu = require('web.FavoriteMenu');

    /**
     * override
     */
    
    // Load perticular filter view.
    function onFavoriteSelected(ev) {
        ev.stopPropagation();
        this.model.dispatch('toggleFilter', ev.detail.payload.itemId);
        if(ev && ev.originalComponent && ev.originalComponent.__owl__ && ev.originalComponent.__owl__.scope && ev.originalComponent.__owl__.scope.item && ev.originalComponent.__owl__.scope.item.context && ev.originalComponent.__owl__.scope.item.context.load_view == 'list'){
            $('.o_list').click();                  
        }
        else if(ev && ev.originalComponent && ev.originalComponent.__owl__ && ev.originalComponent.__owl__.scope && ev.originalComponent.__owl__.scope.item && ev.originalComponent.__owl__.scope.item.context && ev.originalComponent.__owl__.scope.item.context.load_view == 'kanban'){
            $('.o_kanban').click();                  
        }
        else if(ev && ev.originalComponent && ev.originalComponent.__owl__ && ev.originalComponent.__owl__.scope && ev.originalComponent.__owl__.scope.item && ev.originalComponent.__owl__.scope.item.context && ev.originalComponent.__owl__.scope.item.context.load_view == 'calendar'){
            $('.o_calendar').click();               
        }
        else if(ev && ev.originalComponent && ev.originalComponent.__owl__ && ev.originalComponent.__owl__.scope && ev.originalComponent.__owl__.scope.item && ev.originalComponent.__owl__.scope.item.context && ev.originalComponent.__owl__.scope.item.context.load_view == 'pivot'){
            $('.o_pivot').click();           
        }
        else if(ev && ev.originalComponent && ev.originalComponent.__owl__ && ev.originalComponent.__owl__.scope && ev.originalComponent.__owl__.scope.item && ev.originalComponent.__owl__.scope.item.context && ev.originalComponent.__owl__.scope.item.context.load_view == 'graph'){
            $('.o_graph').click();         
        }
        else if(ev && ev.originalComponent && ev.originalComponent.__owl__ && ev.originalComponent.__owl__.scope && ev.originalComponent.__owl__.scope.item && ev.originalComponent.__owl__.scope.item.context && ev.originalComponent.__owl__.scope.item.context.load_view == 'activity'){
            $('.o_activity').click();              
        }
        else if(ev && ev.originalComponent && ev.originalComponent.__owl__ && ev.originalComponent.__owl__.scope && ev.originalComponent.__owl__.scope.item && ev.originalComponent.__owl__.scope.item.context && ev.originalComponent.__owl__.scope.item.context.load_view == 'gantt'){
            $('.o_gantt').click();                
        }
    } 

    FavouriteMenu.prototype.onFavoriteSelected = onFavoriteSelected;
    return FavouriteMenu;

});
