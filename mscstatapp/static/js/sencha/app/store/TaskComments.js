Ext.define('MSCSTAT.store.TaskComments', {
    extend: 'Ext.data.Store',
    model: 'MSCSTAT.model.TaskComments',
    proxy: {
        type: 'rest',
        pageParam: false,
        startParam: false,
        limitParam: false,
        url: 'task_comments',
        reader: {
        	totalProperty: 'count',
            type: 'json',
            successProperty: 'success'
        },
        writer: {
        		writeAllFields: true,
            	encode: false, 
                type: 'json'
        },
		listeners: {
            exception: function(proxy, response, operation){
                Ext.MessageBox.show({
                     title: 'Ошибка изменения данных!',
                     msg: JSON.stringify(Ext.JSON.decode(response.responseText)),
                     icon: Ext.MessageBox.ERROR,
                     buttons: Ext.Msg.OK
                 });
            }
        }
    }
});