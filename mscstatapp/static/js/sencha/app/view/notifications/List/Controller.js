Ext.define('MSCSTAT.view.notifications.List.Controller', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.NotificationsList',

    updateRecord: function(button) {
        var grid = button.up('grid');
        var store = grid.getStore();
        var selection = grid.getSelectionModel().getSelection();
        store.load({
            scope: this,
            callback: function(records, operation, success) {
                if (success) {
                    if (selection.length > 0) {
                        var record_id = selection[0].getId();
                        var record_select = store.getById(record_id);
                        grid.getSelectionModel().deselectAll();
                        grid.getSelectionModel().select(record_select);
                        grid.getView().focusRow(record_select);
                    }
                    else {
                        grid.getSelectionModel().deselectAll();
                        grid.getSelectionModel().select(0);
                        grid.getView().focusRow(0);
                    }
                }
            }
         });
    },
    changePage: function(pagingtoolbar, pageData, eOpts) {
        pagingtoolbar.up('grid').getSelectionModel().select(0);
    },
    selectNotifications: function(selections, model, options) {
        var select = selections.getSelection();
        var store = selections.getStore();
        if (select.length > 0) {
            if (!(select[0].get('read'))){
                select[0].set('read',true);
	            var my = this;
	            store.sync({
	                success : function(data_batch,controller) {
	                	var grid = Ext.getCmp('tabpanel').getActiveTab().down('grid');
	                	grid.getView().focusRow(select[0]);
	                	var info = Ext.ComponentQuery.query('#notifications')[0];
	                    var count_news = my.countMessagesNew(grid);
	                    info.setBadgeText(count_news);
	                },
	                scope: this           
	            });               
            }
        }
    },
    addFilter: function (button) {
        var view = Ext.widget('appNotificationsFilter');
        view.show();
    },
	delFilter: function (button) {
        var grid = button.up('appNotificationsList');
        var store = grid.getStore();
        store.clearFilter();
        button.blur();
        var selection = grid.getSelectionModel().getSelection();
        grid.getSelectionModel().deselectAll();
        grid.getSelectionModel().select(store.getAt(0));
        grid.getView().focusRow(store.getAt(0));
    },
    createMessage: function(button) {
        var view = Ext.widget('appNotificationsEdit');
        view.show();
    },
    addNotifications: function (user,message) {
    	if (user == MSCSTAT.global.Vars.user_id) {
    		return;
    	};
        var store = Ext.data.StoreManager.lookup('Notifications');
        var record = Ext.create('MSCSTAT.model.Notifications');
        record.set('user',user);
        record.set('message',message);
        record.set('date',Ext.Date.format(new Date(), "Y-m-d"));
        store.add(record);
        var my = this;
        store.sync({
            success : function(data_batch,controller) {
                my.taskNotifications();
            },
            scope: this            
        });
        store.commitChanges();//фиксируем иначе накапливаются записи
    },
    countMessagesNew: function (grid){
    	var grid = grid;
    	var store = grid.getStore();
    	store.clearFilter();
    	store.filter('read',false);
    	var count = store.getCount();
    	store.clearFilter();
    	return count;
    },

    //Удаляем соощение
    deleteRecord: function(gridview, el, rowIndex, colIndex, e, rec, rowEl) {
        var store = gridview.getStore();
        Ext.Msg.show({
            title: 'Подтвердите действие!',
            msg: 'Вы действительно хотите удалить запись?',
            buttons: Ext.Msg.YESNO,
            icon: Ext.MessageBox.QUESTION,
            scrollable: false,
            callback: function (btn) {
                if ('yes' === btn) {
                    store.remove(rec);
                    store.sync({
                        success: function (data_batch, controller) {
                            var record_last = store.last();
                            if (record_last != undefined) {
                                gridview.focusRow(record_last);
                                gridview.getSelectionModel().select(record_last);
                            }
                        },
                        scope: this
                    });
                }
            }
        });
    },
    sendMessages: function(button) {
        var my = this;
        var win = button.up('window');
        var form = win.down('form');
        if (form.isValid()) {
        	Ext.Ajax.request({
	            url: '/send_notification/',
	            params:{
	               message: form.getValues().name,
	               recipients: Ext.JSON.encode(form.getValues().recipients),
	               sendsms: form.getValues().sendsms
	            },
	            success: function(response, opts) {
	                var obj = Ext.decode(response.responseText);
	                var content = obj.messages;
	                Ext.Msg.alert('Извещение', content);
	                
	            }
        	});
            win.close();
        }
    }
});