Ext.define('MSCSTAT.store.Priority', {
    extend: 'Ext.data.Store',
    model: 'MSCSTAT.model.Priority',
    autoLoad:true,
    proxy: {
        type: 'rest',
        pageParam: false,
        startParam: false,
        limitParam: false,
        url: 'priority',
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