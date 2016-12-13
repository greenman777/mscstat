Ext.define('MSCSTAT.store.Object', {
    extend: 'Ext.data.Store',
    model: 'MSCSTAT.model.Object',
    autoLoad:false,
    proxy: {
        type: 'rest',
        pageParam: false,
        startParam: false,
        limitParam: false,
        url: 'object',
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