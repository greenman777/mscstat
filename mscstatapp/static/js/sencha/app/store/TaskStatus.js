Ext.define('MSCSTAT.store.TaskStatus', {
    extend: 'Ext.data.Store',
    model: 'MSCSTAT.model.TaskStatus',
    autoLoad:true,
    proxy: {
        type: 'rest',
        pageParam: false,
        startParam: false,
        limitParam: false,
        url: 'task_status',
        reader: {
        	totalProperty: 'count',
            type: 'json',
            successProperty: 'success'
        },
        writer: {
        		writeAllFields: true,
            	encode: false, 
                type: 'json'
        }
    }
});