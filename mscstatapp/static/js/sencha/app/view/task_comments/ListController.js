Ext.define('MSCSTAT.view.task_comments.ListController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.TaskCommentsList',
    
    //Редактируем комментарий
    editRecord: function(gridview, el, rowIndex, colIndex, e, rec, rowEl) {
    	var view = Ext.widget('appTaskCommentsEdit');
    	var record = gridview.getStore().getAt(rowIndex);
 		if(record){
            if (record.get('author')==MSCSTAT.global.Vars.user_id){
    		    var form = view.down('form');
                form.loadRecord(record);
                view.show();
            }
            else {
                Ext.Msg.alert('Предупреждение', 'Редактировать комментарий может только автор!');    
            }
      	}
    },
    //Обнавляем список комментариев
    updateRecord: function(button) {
        var grid_tasks = Ext.getCmp('tabpanel').getActiveTab().down('appTasksList');
        var selection_tasks = grid_tasks.getSelectionModel().getSelection();
        var grid = Ext.getCmp('tabpanel').getActiveTab().down('appTaskCommentsList');
        var store = grid.getStore();
        //если выбрана задача, то обновляем комментарии
        if (selection_tasks.length > 0) {
	        grid.focus();
	        var selection = grid.getSelectionModel().getSelection();
	        store.load({
	            scope: this,
	            callback: function(records, operation, success) {
	                if (success) {
	                    if (selection.length > 0) {
                            var record_id = selection[0].getId();
	                        var record_select = store.getById(record_id);
                            grid.getSelectionModel().select(record_select);
                            grid.getView().focusRow(record_select);
	                    }
	                    else {
	                        grid.getSelectionModel().select(0);
                            grid.getView().focusRow(0);
	                    }
	                        
	                }
	            }
	         });
        }
    },
    //Открываем форму для изменения статуса задачи  
    addRecord: function(button) {
        var store = button.up('appTaskCommentsList').getStore();
        var view = Ext.widget('appTaskCommentsEdit');
        var grid_tasks = Ext.getCmp('tabpanel').getActiveTab().down('appTasksList');
        var selection_tasks = grid_tasks.getSelectionModel().getSelection();
        //если выбрана задача, то открываем форму для добавления комментария
        if (selection_tasks.length > 0) {
            var form = view.down('form');
            form.getForm().setValues({task: selection_tasks[0].getId(),create_date: new Date(),
                                      author: MSCSTAT.global.Vars.user_id
                                    });
            view.show();
        }
        else {
            Ext.Msg.alert('Предупреждение', 'Не выбрана задача!');    
        }
    },
    //Удаляем запись
	deleteRecord: function(gridview, el, rowIndex, colIndex, e, rec, rowEl) {
    	var store = gridview.getStore();
    	var record = store.getAt(rowIndex); 
        var me = this;
        //разрешаем удалять только автору комметария
        if (record.get('author')==MSCSTAT.global.Vars.user_id) {
	    	Ext.MessageBox.confirm('Подтвердите действие!', 'Вы действительно хотите удалить запись?', function(btn){
				if (btn == 'yes') {
		    		store.remove(record);
		    		store.sync();
				}
			});
        }
        else {
            Ext.Msg.alert('Предупреждение', 'Комментарий может удалить только автор!');    
        }
    }
})