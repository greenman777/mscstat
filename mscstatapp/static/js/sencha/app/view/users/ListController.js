Ext.define('MSCSTAT.view.users.ListController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.UsersList',

    //При выборе пользователя отображаем подробности
    selectUser: function(selections, model, options) {
        if (typeof selections.getSelection()[0] != 'undefined'){
            var xtemp = Ext.getCmp('tabpanel').getActiveTab().down('appUsersDetails');
            xtemp.update(selections.getSelection()[0].data);
        }
    },
    changePage: function(pagingtoolbar, pageData, eOpts) {
        pagingtoolbar.up('grid').getSelectionModel().select(0);
    },
    //Открываем форму для назначения задачи пользователю    
    addRecord: function(button) {
        var view_tasks = Ext.widget('appTasksEdit');
        var grid_users = button.up('appUsersList');
        var selection_users = grid_users.getSelectionModel().getSelection();
        // проверяем что пользователь выбран
        if (selection_users.length > 0) {
            var form_tasks = view_tasks.down('form');
            //заполяем у формы обязательные поля
            //var store_status = Ext.data.StoreManager.lookup('TaskStatus');
            //store_status.clearFilter(true);
            form_tasks.getForm().setValues({performer: selection_users[0].getId(),create_date: new Date(),
                author: MSCSTAT.global.Vars.user_id
                //status: store_status.findRecord('name','в работе').getId(),
            });
            view_tasks.show();
        }
        else {
            Ext.Msg.alert('Предупреждение', 'Не выбран пользователь!');    
        }
    },
    //обновляем таблицу пользователей
    updateRecord: function(button) {
        var grid = button.up('grid');
        grid.focus();
        var store = grid.getStore();
        var selection = grid.getSelectionModel().getSelection();
        store.load({
            scope: this,
            callback: function(records, operation, success) {
                if (success) {
                    if (selection.length > 0) {
                        grid.getView().focusRow(selection[0]);
                        grid.getSelectionModel().select(selection);
                    }
                    else {
                        grid.getView().focusRow(0);
                        grid.getSelectionModel().select(0);
                    }
                        
                }
            }
        })
    }
})