Ext.define('MSCSTAT.view.task_comments.EditController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.TaskCommentsEdit',
    
    //Сохраняем новый/измененный комментарий
    saveRecord: function(button) {
    	var win = button.up('window');
        var form = win.down('form');
        var record = form.getRecord();
        var values = form.getValues();
        var grid = Ext.getCmp('tabpanel').getActiveTab().down('appTaskCommentsList');
        var store = grid.getStore();
        var my = this;
        //если форма заполнена корректно
        if (form.isValid()) {
	 		//если запись существует, изменяем запись
	        if (values.id > 0) {
				record.set(values);
				store.sync();
	            grid.getView().focusRow(record);
	            grid.getSelectionModel().select(record);
	        //если запись новая, сохраняем новую запись
			} else {		
				var record = Ext.create('MSCSTAT.model.TaskComments');
				record.set(values);
				store.add(record);
				store.sync({
	    			success : function(data_batch,controller) {
						grid.getView().focusRow(record);  
						grid.getSelectionModel().select(record);
	    			},
	    			scope: this            
				});	
			};
	    	win.close();
        }
	}
})