Ext.define('MSCSTAT.controller.Tasks', {
    extend: 'Ext.app.Controller',
 	views: ['Tasks','tasks.List','tasks.Edit'],
    init: function() {
        this.listen({
            store: {
                 '#tasks_store': {
                     load: this.filterShow
                 }
             }
        });
        this.control({
        	'appTasksList':{
        		selectionchange: this.selectTask
        	},
            'appTasksList actioncolumn[action=edit]': {
                click: this.editRecord
            },
            'appTasksList actioncolumn[action=delete]': {
                click: this.deleteRecord
            },
            'appTasksList button[action=update]': {
                click: this.updateRecord
            },
            'appTasksList button[action=filter_status]': {
                click: this.filterRecord
            },
            'appTasksEdit button[action=save]': {
                click: this.saveRecord
            },
            'appTasksEdit button[action=cancel]': {
            	click: this.closeForm
            }
        });
        this.callParent(arguments);
    }, 
    //Подгружаем историю и комментарии для выбранной задачи    
    selectTask: function(selections, model, options) {
        var store_task_history = Ext.getCmp('tabpanel').getActiveTab().down('appTaskHistoryList').getStore();
        var store_task_comments = Ext.getCmp('tabpanel').getActiveTab().down('appTaskCommentsList').getStore();
        var select_task = selections.getSelection();
        if (select_task.length > 0) {
            var task_id = select_task[0].get('id');
            store_task_history.getProxy().extraParams = {task: task_id};
            store_task_history.load();
            store_task_comments.getProxy().extraParams = {task: task_id};
            store_task_comments.load();
        };
    },
    //Редактируем задачу
    editRecord: function(gridview, el, rowIndex, colIndex, e, rec, rowEl) {
        var view = Ext.widget('appTasksEdit');
        var record = gridview.getStore().getAt(rowIndex);
 		if(record){
        	view.down('form').loadRecord(record);
            view.show();
      	}
    },
    //Обнавляем список задач
    updateRecord: function(button) {
        var grid = button.up('appTasksList');
        var store = grid.getStore();
        grid.focus();
        var my = this;
        var selection = grid.getSelectionModel().getSelection();
        store.load({
            scope: this,
            callback: function(records, operation, success) {
                if (success) {
                    var store_hyst = Ext.getCmp('tabpanel').getActiveTab().down('appTaskHistoryList').getStore();
                    var store_comm = Ext.getCmp('tabpanel').getActiveTab().down('appTaskCommentsList').getStore();
                    store_hyst.removeAll();
                    store_comm.removeAll();
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
    //Сохранияем задачу
    saveRecord: function(button) {
    	var win = button.up('window');
        var form = win.down('form');
        var record = form.getRecord();
        var values = form.getValues();
        //если форма заполнена корректно
        if (form.isValid()) {
	        //если запись уже существует, обновляем
	 		if (values.id > 0) {
	            var grid = Ext.getCmp('tabpanel').getActiveTab().down('appTasksList');
	            var store = grid.getStore();
				record.set(values);
				store.sync();
	            //устанавливаем курсор на измененную задачу
	            grid.getView().focusRow(record);
	            grid.getSelectionModel().select(record);
			} else {
	            //если задача новая, то добавляем ее в базу
	            var store = Ext.data.StoreManager.lookup('Tasks');
				var record = Ext.create('MSCSTAT.model.Tasks');
				record.set(values);
				store.add(record);
                var my = this;
				store.sync({
                    success : function(data_batch,controller) {
                        //my.fireEvent('addNotifications',record.get('performer'),'Для Вас новая задача!: '+record.get('heading'));
                    },
                    scope: this            
                });
			};
            win.close();
        };
	},
    //Удаляем задачу
	deleteRecord: function(gridview, el, rowIndex, colIndex, e, rec, rowEl) {
        var store = gridview.getStore();
    	var record = store.getAt(rowIndex); 
    	Ext.MessageBox.confirm('Подтвердите действие!', 'Вы действительно хотите удалить запись?', function(btn){
			if (btn == 'yes') {
	    		store.remove(record);
	    		store.sync({
                    success : function(data_batch,controller) {
                        var store_hyst = Ext.getCmp('tabpanel').getActiveTab().down('appTaskHistoryList').getStore();
                        var store_comm = Ext.getCmp('tabpanel').getActiveTab().down('appTaskCommentsList').getStore();
                        store_hyst.removeAll();
                        store_comm.removeAll();
                        var record_last = store.last();
                        if (record_last != undefined) {
                            gridview.focusRow(record_last);  
                            gridview.getSelectionModel().select(record_last);    
                        };
                    },
                    scope: this            
                });
			}
    	});	
    }, 
    //Обновляем статус текущей задачи
    updateStatus: function(status_id) {
        var grid = Ext.getCmp('tabpanel').getActiveTab().down('appTasksList');
        var store = grid.getStore();
        var selection = grid.getSelectionModel().getSelection();
        if (selection.length > 0) {
            var record = selection[0];
            record.set('status',status_id);
            store.sync({
                success : function(data_batch,controller) {
                    var complet = Ext.getCmp('tabpanel').getActiveTab().complet;
			        if (complet == undefined) {
			            complet = true;
			        }
                    this.filterStore(grid.down('#filter_status'),!complet);
                },
                scope: this            
            });
        }
    },
    //Закрываем форму
    closeForm: function(button) {
    	button.up('window').close();
    },
    //фильтруем записи при старте
    filterShow: function(store) {
        this.filterStore(Ext.getCmp('tabpanel').getActiveTab().down('appTasksList').down('#filter_status'),false);
    },
    //фильтр при нажатии кнопки фильтрации
    filterRecord: function(button) {
        var complet = button.up('appTasks').complet;
        if (complet == undefined) {
            complet = true;
        }
        this.filterStore(button,complet);
    },
    //фильтруем записи
    filterStore: function(button,complet) {
        var grid = button.up('gridpanel');
        var store = grid.getStore();
        store.clearFilter(true);
        var my = this;
        if (complet) {
            store.filter(function(r) {
                var value = r.get('status');
                return (value == my.idStatus('выполнена'));
            });
        }
        else {
            store.filter(function(r) {
                var value = r.get('status');
                return (value == my.idStatus('в работе') || value == my.idStatus('на проверку') || value == my.idStatus('отклонена'));
            });
        };
        var record_last = store.last();
        if (record_last != undefined) {
            grid.getSelectionModel().select(record_last);
        }   
        else {
            var store_hyst = grid.up('tabpanel').down('appTaskHistoryList').getStore();
            var store_comm = grid.up('tabpanel').down('appTaskCommentsList').getStore();
            store_hyst.removeAll();
            store_comm.removeAll();
        }
    },
    //возвращаем id статуса задачи по названию
    idStatus: function(status_name) {
        var store_status = Ext.data.StoreManager.lookup('TaskStatus');
        store_status.clearFilter(true);
        var status_id = store_status.findRecord('name',status_name).getId(); 
        return status_id;
    }
});