Ext.define('MSCSTAT.store.Notifications', {
    extend: 'Ext.data.Store',
    model: 'MSCSTAT.model.Notifications',
    autoLoad:true,
    pageSize: 20,
    proxy: {
        type: 'rest',
        url: 'notifications',
        pageParam: 'page',
        startParam: 'start',
        limitParam: 'limit',
        reader: {
        	type: 'json',
            totalProperty: 'count',
            rootProperty: 'results',
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